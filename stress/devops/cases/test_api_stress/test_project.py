import pytest
from libs.log_obj import LogObj
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = LogObj().get_logger()


def test_create_project(devops_api_stress_common):
    pass
