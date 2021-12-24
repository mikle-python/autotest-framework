import pytest
import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from stress.ecos.common.common import minio_files, get_file_md5
from libs.log_obj import LogObj
from libs.minio_obj import MinIoObj
from prettytable import PrettyTable

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def minio_test_data(component_test_data):
    return component_test_data("minio")


@pytest.fixture(scope='session')
def minio_obj(minio_test_data):
    return MinIoObj(minio_test_data['end_point'], minio_test_data['access_key'], minio_test_data['secret_key'],
                    minio_test_data['secure'])


@pytest.fixture(scope='function')
def minio_data_files(minio_test_data):
    return minio_files(minio_test_data['file_upload_path'], minio_test_data['minio_files_quantity'],
                       minio_test_data['min_size'], minio_test_data['max_size'])


def test_minio_upload_download(minio_obj, minio_data_files, minio_test_data):
    test_minio_upload_download.__doc__ = 'Test start, minio stress test !'
    logger.info(test_minio_upload_download.__doc__)
    start_time = datetime.datetime.now()
    table_md5 = PrettyTable(['ObjectName', 'upload_file_md5', 'download_file_md5'])

    logger.debug("Start upload ...")
    pool = ThreadPoolExecutor(max_workers=20)
    futures = []
    for minio_data_object_name, minio_data_object_file_path in minio_data_files.items():
        futures.append(pool.submit(minio_obj.upload_file, minio_test_data['bucket_name'], minio_data_object_name,
                                   minio_data_object_file_path['file_path']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    logger.debug("Finish upload ...")
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('Upload {file_number} take time: {time}'.format(file_number=len(minio_data_files),time=take_time))

    logger.debug("Start download ...")
    start_time = datetime.datetime.now()
    pool_download = ThreadPoolExecutor(max_workers=20)
    futures_download = []
    for download_object_name, _ in minio_data_files.items():
        download_file_path_name = os.path.join(minio_test_data['file_download_path'], download_object_name)
        futures_download.append(pool_download.submit(minio_obj.download_file, minio_test_data['bucket_name'],
                                                     download_object_name, download_file_path_name))
    pool_download.shutdown()
    for future in as_completed(futures_download):
        future.result()
    logger.debug("Finish download ...")
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('Download {file_number} take time: {time}'.format(file_number=len(minio_data_files), time=take_time))

    logger.info("Start comparing original/download file md5 value !")
    md5_different = []
    for object_name, file_data_md5 in minio_data_files.items():
        md5_value = get_file_md5(os.path.join(minio_test_data['file_download_path'], object_name))
        if md5_value != file_data_md5['file_md5']:
            md5_different.append({object_name: {'before': file_data_md5['file_md5'], 'after': md5_value}})
            table_md5.add_row([object_name, file_data_md5['file_md5'], md5_value])

    if md5_different:
        logger.warning("\n{0}".format(table_md5))
        raise Exception("Appear md5 original/download error !")

    logger.info("Original/Download file md5 test pass !")
