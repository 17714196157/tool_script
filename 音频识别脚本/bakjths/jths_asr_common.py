# -*- coding:utf-8 -*-
# /usr/bin/python2

import requests
import datetime
import hashlib
import json
import os
import util_func


def get_session_key(cur_time):
    src_str = cur_time + "28c173ce82c7c7ef5de62f0c52ebcc54"
    m2 = hashlib.md5(src_str.encode())
    md5_rst = m2.hexdigest()
    return md5_rst


def recog_single_8k(wav_file):
    url = "http://api.hcicloud.com:8880/asr/Recognise"
    cur_day = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_time1 = datetime.datetime.now().strftime('%H:%M:%S')
    cur_time = cur_day + " " + cur_time1
    session_key_str = get_session_key(cur_time)
    header = {'x-app-key': "745d540c",
              'x-sdk-version': "5.0",
              'x-request-date': cur_time,
              'x-result-format': "json",
              'x-task-config': "capkey=asr.cloud.freetalk,audioformat=pcm8k16bit,domain=telecom",   # ,property=chinese_8k_common
              'x-session-key': session_key_str,
              'x-udid': "101:1234567890"
              }

    wave_data = open(wav_file, "rb")
    r = requests.post(url,  headers=header, data=wave_data)
    if r.status_code == 200:
        r.encoding = "utf-8"  # r.apparent_encoding
        result = json.loads(r.text)
        result_text = result['ResponseInfo']['Result']['Text']
        result_score = result['ResponseInfo']['Result']['Score']
        result_code = result['ResponseInfo']['ErrorNo']
        return result_code, result_text, result_score
    else:
        return None, None, None



def recog_single_16k(wav_file):
    url = "http://api.hcicloud.com:8880/asr/Recognise"
    cur_day = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_time1 = datetime.datetime.now().strftime('%H:%M:%S')
    cur_time = cur_day + " " + cur_time1
    session_key_str = get_session_key(cur_time)
    header = {'x-app-key': "745d540c",
              'x-sdk-version': "5.0",
              'x-request-date': cur_time,
              'x-result-format': "json",
              'x-task-config': "capkey=asr.cloud.freetalk,audioformat=pcm16k16bit,domain=common",
              'x-session-key': session_key_str,
              'x-udid': "101:1234567890"
              }

    wave_data = open(wav_file, "rb")
    r = requests.post(url,  headers=header, data=wave_data)
    if r.status_code == 200:
        r.encoding = r.apparent_encoding
        result = json.loads(r.text)
        result_text = result['ResponseInfo']['Result']['Text']
        result_score = result['ResponseInfo']['Result']['Score']
        result_code = result['ResponseInfo']['ErrorNo']
        return result_code, result_text, result_score
    else:
        return None, None, None



exts = ["wav"]

def do_pridict_jths_1order(src_dir):
    errors_sum = 0.0
    time_avg = 0
    len_refs = 0
    badCnt = 0
    num_ins = 0
    nullCnt = 0

    for file in os.listdir(src_dir):
        wav_filePath = os.path.join(src_dir, file)
        if any(wav_filePath.lower().endswith("." + ext) for ext in exts):
            # print('cur file: ', file)
            Labels_filePath = wav_filePath.replace('.wav', '.txt')
            label_true1 = util_func.get_label_true_markSys(Labels_filePath)
            # ----------------------------------------
            startTime = datetime.datetime.now()
            _, label_xf, _ = recog_single_8k(wav_filePath)
            endTime = datetime.datetime.now()
            d = (endTime - startTime)
            usedTimeMs = d.total_seconds() * 1000
            time_avg += usedTimeMs
            #print('used time: %.2fms' % usedTimeMs)
            # ----------------------------------------
            if type(label_xf) == int:
                label_xf = str(label_xf)
                # print("-------%s-------"%label_xf)
            if len(label_xf) == 0 or label_xf == {}:
                nullCnt += 1
                label_xf = ""
            label_predict = util_func.rm_flags(label_xf.encode("utf-8"))
            label_true = util_func.rm_flags(label_true1)
            # ----------------------------------------------
            print("\ngroundtruth label: %s\npredict label: %s" % (label_true, label_predict))
            errors, len_ref = util_func.char_errors(label_true, label_predict)
            print("Current error rate [%s] = %f" % ("cer", errors))
            errors_sum += errors
            len_refs += len_ref
            num_ins += 1
            print("Error rate [%s] (%d/?) = %f" % ("cer", num_ins, errors_sum / len_refs))
    print('badCnt: %d' % (badCnt))
    print('nullCnt: %d' % (nullCnt))
    print('fileCnt: %d' % (num_ins))
    print("Final error rate [%s] (%d/?) = %f" % ("cer", num_ins, errors_sum / len_refs))
    print('time_avg: %.2f' % (time_avg / num_ins))



def do_pridict_jths_1order_no_gt(src_dir):
    errors_sum = 0.0
    time_avg = 0
    len_refs = 0
    badCnt = 0
    num_ins = 0
    nullCnt = 0

    for file in os.listdir(src_dir):
        wav_filePath = os.path.join(src_dir, file)
        if any(wav_filePath.lower().endswith("." + ext) for ext in exts):
            # ----------------------------------------
            startTime = datetime.datetime.now()
            _, label_xf, _ = recog_single_8k(wav_filePath)
            endTime = datetime.datetime.now()
            d = (endTime - startTime)
            usedTimeMs = d.total_seconds() * 1000
            time_avg += usedTimeMs
            # ----------------------------------------
            if type(label_xf) == int:
                label_xf = str(label_xf)
                # print("-------%s-------"%label_xf)
            if len(label_xf) == 0 or label_xf == {}:
                nullCnt += 1
                label_xf = ""
            label_predict = util_func.rm_flags(label_xf.encode("utf-8"))
            print("\ncur file: %s, predict label: %s" % (file, label_predict))
            num_ins += 1
    print('badCnt: %d' % (badCnt))
    print('nullCnt: %d' % (nullCnt))
    print('fileCnt: %d' % (num_ins))
    print('time_avg: %.2f' % (time_avg / num_ins))


if __name__ == '__main__':
    wav_file = "./data/wavs/16k/hard/产权是多少年的.wav"
    #result_code, result_text, result_score = recog_single_16k(wav_file)
    #print("rst_txt = ", result_text)


    src_folder = r'D:\MLproject\326'
    do_pridict_jths_1order(src_folder)
