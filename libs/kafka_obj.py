from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from libs.log_obj import LogObj
from utils.util import generate_random_string
from utils.times import sleep
from utils.decorator import print_for_call, retry
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = LogObj().get_logger()


class KafkaProducerObj(object):
    _producer_session = None
    _kafka_config = None

    def __init__(self, brokers):
        self.brokers = brokers

    def __del__(self):
        self.producer_session.close(timeout=150000)

    @property
    def kafka_config(self):
        if self._kafka_config is None:
            self._kafka_config = {
                'bootstrap_servers': self.brokers
            }
        return self._kafka_config

    @property
    def producer_session(self):
        if self._producer_session is None:
            self._producer_session = KafkaProducer(bootstrap_servers=self.kafka_config['bootstrap_servers'])
        return self._producer_session

    @retry(tries=10, delay=10)
    def message_sync_check(self, send_message_obj, timeout=20):
        return send_message_obj.get(timeout=timeout)

    @retry(tries=10, delay=10)
    @print_for_call
    def send_sync_message(self, topic_name, message_min_size, message_max_size):
        message_send = "Test kafka random message -> {}".\
            format(generate_random_string(message_max_size, message_min_size))
        send_future = self.producer_session.send(topic_name, message_send.encode('utf8'))
        try:
            message = self.message_sync_check(send_future)
            logger.info("Send message to [topic: {} partition: {}]"
                        " and the message length is {}".format(message.topic, message.partition, len(message_send)))

        except Exception as e:
            logger.warning('Message delivery failed: {}'.format(str(e)))
            raise e

    @retry(tries=10, delay=10)
    @print_for_call
    def send_async_message(self, topic_name, message_min_size, message_max_size):
        message_send = "Test kafka random message -> {}".\
            format(generate_random_string(message_max_size, message_min_size))
        self.producer_session.send(topic_name, message_send.encode('utf8')).add_callback(self.on_send_success).\
            add_errback(self.on_send_error)
        self.producer_session.flush()

    def on_send_success(self, message):
        logger.info("Send message to [topic: {} partition: {}]".format(message.topic, message.partition))

    def on_send_error(self, excp):
        logger.warning('I am an err back: {}'.format(excp))
        # handle exception

    @print_for_call
    def send_async_message_with_multiple_topic(self, topic_name, topic_quantity, message_min_size, message_max_size):
        pool = ThreadPoolExecutor(max_workers=50)
        futures = []
        for topic_number in range(topic_quantity):
            futures.append(pool.submit(self.send_async_message, "{}_{}".format(topic_name, topic_number),
                                       message_min_size, message_max_size))
        pool.shutdown()
        for future in as_completed(futures):
            future.result()

    @print_for_call
    def send_async_multiple_messages_with_multiple_topics(self, topic_name, topic_quantity, message_min_size,
                                                         message_max_size, message_quantity):
        pool = ThreadPoolExecutor(max_workers=50)
        futures = []
        for _ in range(message_quantity):
            futures.append(pool.submit(self.send_async_message_with_multiple_topic, topic_name, topic_quantity,
                                       message_min_size, message_max_size))
        pool.shutdown()
        for future in as_completed(futures):
            future.result()


class KafkaConsumerObj(object):
    _consumer_session = None
    _kafka_config = None

    def __init__(self, brokers, group_id):
        self.brokers = brokers
        self.group_id = group_id

    # def __del__(self):
    #     self.consumer_session.close()

    @property
    def kafka_config(self):
        if self._kafka_config is None:
            self._kafka_config = {
                'bootstrap_servers': self.brokers,
                'session.timeout.ms': 30000,
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest'
            }
        return self._kafka_config

    @property
    def consumer_session(self):
        if self._consumer_session is None:
            self._consumer_session = KafkaConsumer(bootstrap_servers=self.kafka_config['bootstrap_servers'],
                                                   group_id=self.kafka_config['group.id'],
                                                   auto_offset_reset=self.kafka_config['auto.offset.reset'])
        return self._consumer_session

    @retry(tries=30, delay=20)
    @print_for_call
    def receive_message(self, client_id, topic_names):
        self.consumer_session.subscribe(topic_names)
        no_messages = 0
        while True:
            try:
                messages_left = sum(self.message_left(topic_name) for topic_name in topic_names)
            except TypeError:
                logger.info("Ignore Type error !")
                messages_left = 1

            if messages_left > 0:
                no_messages = 0
                message = self.consumer_session.poll(timeout_ms=15000)
                logger.info("Started to receive messages from topics !")

                if message == {}:
                    raise Exception("Message get fail !")

                for _, receive_messages in message.items():
                    for receive_message in receive_messages:
                        logger.info("Received messages length is {} from [topic: {} partition: {}]".format
                                    (len(receive_message.value), receive_message.topic, receive_message.partition))
            else:
                logger.info("Client:{} already got message amount is {}".
                            format(client_id, sum(self.message_committed_offset(topic_name) for topic_name in
                                                  topic_names)))
                logger.info("Client:{}'s total messages amount is {}".
                            format(client_id, sum(self.end_offsets(topic_name)for topic_name in topic_names)))
                logger.debug("Repeat get messages after 10s !")
                sleep(10)
                no_messages += 1
                if no_messages > 30:
                    logger.warning("No more messages after 5 minutes, exit from consumer client")
                    break

    def get_partitions_by_topic(self, topic_name):
        return list(self.consumer_session.partitions_for_topic(topic_name))

    def get_topic_partitions(self, topic_name):
        return [TopicPartition(topic_name, partition) for partition in self.get_partitions_by_topic(topic_name)]

    def end_offsets(self, topic_name):
        topic_partitions = self.get_topic_partitions(topic_name)
        return sum([amount for _, amount in self.consumer_session.end_offsets(topic_partitions).items()])

    def message_committed_offset(self, topic_name):
        topic_partitions = self.get_topic_partitions(topic_name)
        return sum([self.consumer_session.committed(topic_partition) for topic_partition in topic_partitions])

    def message_left(self, topic_name):
        total_offsets = self.end_offsets(topic_name)
        current_offsets = self.message_committed_offset(topic_name)

        return total_offsets - current_offsets


if __name__ == '__main__':
    import datetime

    brokers = "192.168.1.236:32111"
    kf = KafkaProducerObj(brokers)
    start_time = datetime.datetime.now()
    for _ in range(1, 30):
        kf.send_sync_message("topic1c45", 100000, 100001)

    end_time = datetime.datetime.now()
    take_time = end_time-start_time

    print("cost times: {}".format(take_time))
    # kc = KafkaConsumerObj(brokers, "test_kafka")
    # # kc.message_committed_offset('topic13')
    # kc.receive_message(['topic1c45'])
    # pats = kc.message_left("test_kafka_88_8")
    #
    # print("kafka left: {}".format(pats))
