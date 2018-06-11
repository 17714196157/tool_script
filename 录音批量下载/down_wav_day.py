#encoding:utf-8
import time
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import logging
import logging.handlers

def creat_app_log(log_path='/home/psc/audio/', level=logging.INFO):
    """
    创建app的日志handle
    :param: 日志路径:
    :return: 日志logger
    """
    LOGGING_MSG_FORMAT = '[%(asctime)s] [%(filename)s[line:%(lineno)d]] [%(levelname)s] [%(message)s]'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=level, format=LOGGING_MSG_FORMAT, datefmt=LOGGING_DATE_FORMAT)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    LOG_PATH = os.path.join(log_path, "down_wav.log")
    fileHandler = logging.handlers.WatchedFileHandler(LOG_PATH)
    fileHandler.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
    logger = logging.getLogger()
    logger.addHandler(fileHandler)
    return logger


def do_down_wav(url, name, dirpath=r"D:\tmpQQ"):
    """
    下载单个网络上录音文件
    :param url:
    :param name:
    :return:
    """
    # print("下载地址为：", url, "文件名为：", name)
    res = requests.get(url=url)
    filepath = os.path.join(dirpath, name)

    with open(filepath, mode="bw") as f:
        f.write(res.content)


def do_down_wav_content(filepath, mean):
    """
    下载单个网络上录音文件
    :param url:
    :param name:
    :return:
    """
    # print("下载地址为：", url, "文件名为：", name)
    with open(filepath, mode='w', encoding='utf-8') as f:
        f.write(mean)


def run(logger):
    date = time.time()
    date = time.strftime("%Y%m%d", time.localtime(date))
    voicedata_url = "http://yw.guiji.ai/voicelist/{date}.txt".format(date=date)
    root_path = os.path.join("/home/psc/audio/data", str(date))
    os.makedirs(root_path, exist_ok=True)
    voicedata_path = os.path.join(root_path, date + ".txt")
    print(voicedata_url, root_path)
    logger.info(str(voicedata_url) + " root_path=" + str(root_path) + "date:" + str(date))
    response = requests.get(url=voicedata_url)
    response.encoding = "utf-8"
    do_down_wav_content(voicedata_path, str(response.text))

    # input("!!!!!!!!!!!!")
    executor = ThreadPoolExecutor(20)
    with open(voicedata_path, mode='r', encoding="utf-8") as f:
        n = 0
        future_list = []
        for nodetmp in f:
            urltmp = nodetmp.split("|")[0]
            mean = nodetmp.split("|")[1].strip().replace("\s", "").replace("。", "").\
                replace(".", "").replace("，", "").replace(",", "").replace("？", "").replace("?", "")
            url = urltmp.strip()
            filename = url.strip().split("/")[-1]
            if divmod(n, 10000)[1] == 0:
                print(n, url, filename)
                logger.info("n=" + str(n) + " root_path=" + str(url) + " filename=" + str(filename) + "date:" + str(date))

            future = executor.submit(do_down_wav, url, filename, root_path)
            do_down_wav_content(os.path.join(root_path, filename) + ".txt", mean)
            n = n + 1
            future_list.append(future)
    # executor.shutdown()
    all_n = len(future_list)
    thread_n = 0
    while thread_n != all_n:
        thread_n = 0
        for future in future_list:
            if future.done():
                thread_n = thread_n + 1
        time.sleep(60)
        schedule = int(thread_n * 100 / all_n)
        print("schedule:", schedule, thread_n, all_n)
        logger.info(
            "schedule=" + str(schedule) + " thread_n=" + str(thread_n) + " all_n=" + str(all_n) + "date:" + str(date))


if __name__ == "__main__":
    date = time.time()
    date = time.localtime(date)
    logger = creat_app_log()
    if divmod(date.tm_mday, 2)[1] == 0:
        run(logger)
        pass
    else:
        run(logger)
    pass

'''  文件内容格式 说明
http://global.res.btows.com/data/record/152102312220180314/13956221841_1521023058_10636943_9.wav
http://global.res.btows.com/data/record/152102311720180314/13531611068_1521023078_11291188_3.wav
http://global.res.btows.com/data/record/152102310920180314/18715106309_1521023045_10427874_5.wav
http://global.res.btows.com/data/record/152102310320180314/13889870918_1521022977_10606027_10.wav
http://global.res.btows.com/data/record/152102310320180314/13889870918_1521022977_10606027_6_0.wav
'''
