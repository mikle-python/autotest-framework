from minio import Minio
from minio.error import MinioException
from libs.log_obj import LogObj
from utils.decorator import print_for_call, retry

logger = LogObj().get_logger()


class MinIoObj:
    _minio_session = None

    def __init__(self, end_point, access_key, secret_key, secure=False):
        self.end_point = end_point
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure

    @property
    def minio_session(self):
        if self._minio_session is None:
            self._minio_session = Minio(self.end_point, access_key=self.access_key, secret_key=self.secret_key
                                        , secure=self.secure)
        return self._minio_session

    @print_for_call
    def create_bucket(self, bucket_name):
        if not self.is_bucket_exist(bucket_name):
            try:
                self.minio_session.make_bucket(bucket_name)
            except MinioException:
                logger.warning("Create bucket <{bucket_name}> fail !")
                return False
            return True

        logger.info("Bucket <{bucket_name}> has already exist !")

    def list_all_buckets(self):
        return self.minio_session.list_buckets()

    def is_bucket_exist(self, bucket_name):
        return self.minio_session.bucket_exists(bucket_name)

    def remove_bucket(self, bucket_name):
        self.minio_session.remove_bucket(bucket_name)

    @retry(tries=10, delay=10)
    @print_for_call
    def upload_file(self, bucket_name, object_name, file_path):
        self.create_bucket(bucket_name)
        try:
            self.minio_session.fput_object(bucket_name, object_name, file_path)
        except MinioException as e:
            logger.warning("Upload object <{}> to bucket <{}> fail".format(object_name, bucket_name))
            raise e
        logger.info("Upload object <{}> to bucket:{} successfully !".format(object_name, bucket_name))

    @retry(tries=10, delay=10)
    @print_for_call
    def download_file(self, bucket_name, object_name, file_path):
        self.minio_session.fget_object(bucket_name, object_name, file_path)

    def get_object(self, bucket_name, object_name):
        return self.minio_session.get_object(bucket_name, object_name)

    def get_objects_by_bucket(self, bucket_name):
        objects = []
        for bucket_obj in self.minio_session.list_objects(bucket_name):
            objects.append(bucket_obj.object_name)
        return objects

    def remove_object(self, bucket_name, object_name):
        self.minio_session.remove_object(bucket_name, object_name)

    def multiple_upload_files(self):
        pass


if __name__ == '__main__':
    ep = "minio-0.minio-headless.venus-plugin.svc.cluster.local:32759"
    ak = "password"
    sk = "password"
    # minioClient = MinIoObj(e_point, a_key, s_key)
    #
    # bucket = "test"
    # ac = minioClient.get_objects_by_bucket(bucket)
    # print(ac)
    # ep = 'play.min.io'
    # ak = "Q3AM3UQ867SPQQA43P2F"
    # sk = "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
    cl = MinIoObj(ep, ak, sk)
    bucket_name = "kwangkwangkwang"

    cl.is_bucket_exist(bucket_name)
