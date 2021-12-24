import pytest
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from libs.kafka_obj import KafkaConsumerObj, KafkaProducerObj
from prettytable import PrettyTable

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def kafka_test_data(component_test_data):
    return component_test_data("kafka")


@pytest.fixture(scope='session')
def kafka_producers_obj(kafka_test_data):
    return [{obj_id: KafkaProducerObj(kafka_test_data['brokers'])} for obj_id in
            range(kafka_test_data['client_quantity'])]


@pytest.fixture(scope='session')
def kafka_consumers_obj(kafka_test_data):
    return [{obj_id: KafkaConsumerObj(kafka_test_data['brokers'], kafka_test_data['group_id'])}
            for obj_id in range(kafka_test_data['client_quantity'])]


@pytest.fixture(scope='function')
def kafka_topic_message_quantity(kafka_test_data):
    kafka_topic_message_quantity = kafka_test_data['message_quantity'] // kafka_test_data['topic_quantity']

    if kafka_topic_message_quantity < 1:
        kafka_topic_message_quantity = 1
    return kafka_topic_message_quantity


@pytest.fixture(scope='function')
def kafka_topic_client_quantity(kafka_test_data):
    if kafka_test_data['client_quantity'] > kafka_test_data['topic_quantity']:
        logger.warning("The client quantity must be lower than topic_quantity !")
        raise Exception("The client quantity must be lower than topic_quantity !")

    return kafka_test_data['topic_quantity'] // kafka_test_data['client_quantity']


def test_kafka(kafka_producers_obj, kafka_consumers_obj, kafka_topic_client_quantity, kafka_topic_message_quantity,
               kafka_test_data):
    if kafka_test_data['mode'] == 'producer':
        test_kafka.__doc__ = 'Test start, kafka producer stress test !'
        logger.info(test_kafka.__doc__)
        table_kafka_1 = PrettyTable(['TotalClients', 'TotalTopics', 'TotalMessages'])
        table_kafka_2 = PrettyTable(['Topics/1 Client', 'MessagesNumber/1 Topic'])
        table_kafka_1.add_row([kafka_test_data['client_quantity'], kafka_test_data['topic_quantity'],
                               kafka_test_data['message_quantity']])
        table_kafka_2.add_row([kafka_topic_client_quantity, kafka_topic_message_quantity])
        logger.info("Test parameters are :\n{}\n{}".format(table_kafka_1, table_kafka_2))

        start_time = datetime.datetime.now()

        pool = ThreadPoolExecutor(max_workers=kafka_test_data['client_quantity'])
        futures = []

        for kafka_producer_obj_dict in kafka_producers_obj:
            for obj_id, kafka_producer_obj in kafka_producer_obj_dict.items():
                futures.append(pool.submit(kafka_producer_obj.send_async_multiple_messages_with_multiple_topics,
                                           "{}_{}".format(kafka_test_data['topic'], str(obj_id)),
                                           kafka_topic_client_quantity, kafka_test_data['message_min_size'],
                                           kafka_test_data['message_max_size'], kafka_topic_message_quantity))

        pool.shutdown()
        for future in as_completed(futures):
            future.result()

        end_time = datetime.datetime.now()
        take_time = end_time - start_time
        logger.info(f"Send {kafka_test_data['message_quantity']} take time: {take_time}")

        logger.info(f"Send {kafka_test_data['message_quantity']} messages successfully !")

    elif kafka_test_data['mode'] == 'consumer':
        test_kafka.__doc__ = 'Test start, kafka consumer stress test !'
        logger.info(test_kafka.__doc__)

        pool = ThreadPoolExecutor(max_workers=kafka_test_data['client_quantity'])
        futures = []
        for kafka_consumer_obj_dict in kafka_consumers_obj:
            for obj_id, kafka_consumer_obj in kafka_consumer_obj_dict.items():
                futures.append(pool.submit(kafka_consumer_obj.receive_message, obj_id,
                                           ["{}_{}_{}".format(kafka_test_data['topic'], str(obj_id), topic_number) for
                                            topic_number in range(kafka_topic_client_quantity)]))

        pool.shutdown()
        for future in as_completed(futures):
            future.result()
    else:
        raise Exception("No mode selected !")
