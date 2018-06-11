import time, os
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor


def do_down_wav(url, name, dirpath=r"D:\tmpQQ"):
    """
    下载单个网络上录音文件
    :param url:
    :param name:
    :return:
    """
    print("下载地址为：", url, "文件名为：", name)
    res = requests.get(url=url)
    with open(os.path.join(dirpath, str(name)), mode='bw') as f:
        f.write(res.content)


executor = ThreadPoolExecutor(30)
rootpath = r"D:\tmp0518"
with open("20180518_emptycontent.txt", mode='r') as f:
    n = 0
    for nodetmp in f:
        url = nodetmp.strip()
        # print(n, url)
        filename = url.strip().split("/")[-1]
        if True:
            date = float(filename.strip().split("_")[1])
            date = time.strftime("%Y-%m-%d", time.localtime(date))
            dirpath = os.path.join(rootpath, str(date))
        else:
            dirpath = rootpath
        if not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        print(n, url, filename, date)
        future = executor.submit(do_down_wav, url, filename, dirpath)
        n = n+1

    executor.shutdown()
	
	
'''  文件内容格式 说明
http://global.res.btows.com/data/record/152102312220180314/13956221841_1521023058_10636943_9.wav
http://global.res.btows.com/data/record/152102311720180314/13531611068_1521023078_11291188_3.wav
http://global.res.btows.com/data/record/152102310920180314/18715106309_1521023045_10427874_5.wav
http://global.res.btows.com/data/record/152102310320180314/13889870918_1521022977_10606027_10.wav
http://global.res.btows.com/data/record/152102310320180314/13889870918_1521022977_10606027_6_0.wav
'''