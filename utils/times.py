import datetime
import time
import pytz
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA


def sleep(sleep_time):
    """
    Print a progress bar, total value: sleep_time(seconds)
    :param sleep_time:
    :return:
    """

    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=sleep_time).start()
    if sleep_time < 1:
        pbar.update(sleep_time)
        time.sleep(sleep_time)
    else:
        for i in range(sleep_time):
            pbar.update(1 * i + 1)
            time.sleep(1)
    pbar.finish()


def str_to_datetime(st, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(st, fmt)


def datetime_to_str(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(fmt)


def convert_timezone(dtime, tz=pytz.timezone('Asia/Shanghai')):
    return dtime.astimezone(tz=tz)


def time_str():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    print(sleep(0.9))