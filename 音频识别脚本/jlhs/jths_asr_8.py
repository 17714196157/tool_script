# -*- coding:utf-8 -*-

"""
File Name : 'jths_asr'.py
Description:
Author: 'weicheng'
Date: '2018/3/21' '下午5:57'
"""
import requests
import datetime
import hashlib
import json
import os


result_file = open('jths-8k.txt', 'w', encoding='utf-8')


def get_session_key(cur_time):
    src_str = cur_time + "28c173ce82c7c7ef5de62f0c52ebcc54"
    m2 = hashlib.md5(src_str.encode())
    md5_rst = m2.hexdigest()
    return md5_rst


def recog_single(wav_file):
    url = "http://api.hcicloud.com:8880/asr/Recognise"
    cur_day = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_time1 = datetime.datetime.now().strftime('%H:%M:%S')
    cur_time = cur_day + " " + cur_time1
    session_key_str = get_session_key(cur_time)
    header = {'x-app-key': "745d540c",
              'x-sdk-version': "5.0",
              'x-request-date': cur_time,
              'x-result-format': "json",
              'x-task-config': "capkey=asr.cloud.freetalk,audioformat=pcm8k16bit,domain=telecom",
              'x-session-key': session_key_str,
              'x-udid': "101:1234567890"
              }

    wave_data = open(wav_file, "rb")
    r = requests.post(url,  headers=header, data=wave_data)
    if r.status_code == 200:
        r.encoding = r.apparent_encoding
        # print(r.text)
        result = json.loads(r.text)
        result_text = result['ResponseInfo']['Result']['Text']
        result_score = result['ResponseInfo']['Result']['Score']
        result_code = result['ResponseInfo']['ErrorNo']
        return result_code, result_text, result_score


# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         for dir in dirs:
#             if dir.endswith(('2', '4', '6', '8')):
#                 path = os.path.join(file_dir, dir)
#
#         return files

if __name__ == '__main__':
    recog_single(r'D:\MLproject\qq_try\音频识别脚本\input\8k\13505713525_1502762667_84812.wav')
    # recog_single('/Users/weicheng/Documents/15335178985_1521615997_8372761_12.wav')
    #recog_single('/Users/weicheng/Documents/15335178985_1521615997_8372761_15.wav')
    # file_list = file_name('/Users/weicheng/project/asr-test/test_wav')