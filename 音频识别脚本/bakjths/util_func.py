# -*- coding: utf-8 -*-

import os, re
import codecs
import soundfile
import json
import numpy as np

exts = ["wav"]


def rm_flags(sentence):
    if sentence != None:
        out_str = ""
        xx = u"([\u4e00-\u9fff]+)"
        pattern = re.compile(xx)
        results = pattern.findall(sentence.decode("utf-8"))
        for result in results:
            out_str += result
        return out_str.encode("utf-8")
    else:
        return ""


# 测试匹配中文信息
def TestReChinese():
    temp = u"数据结构模版----单链表SimpleLinkList[带头结点&&面向对象设计思想](C语言实现)"
    #temp = source.decode('utf8')
    print("同时匹配中文英文")

    xx = u"([\w\W\u4e00-\u9fff]+)"
    pattern = re.compile(xx)
    results = pattern.findall(temp)
    for result in results:
        print(result)
    print("只匹配中文")
    xx = u"([\u4e00-\u9fff]+)"
    pattern = re.compile(xx)
    results = pattern.findall(temp)
    for result in results:
        print(result)


def get_label_true_markSys(txt_file):
    if os.path.exists(txt_file):
        label_true = ''
        lineCnt = 0
        with open(txt_file, 'r') as fr:
            for line in fr:
                lineCnt += 1
                if (lineCnt == 1):
                    line = line.strip('\r\n')
                    label_true = line.replace(' ','')
    else:
        label_true = os.path.basename(txt_file.replace(".txt", ""))
    # return label_true
    return rm_flags(label_true)


def create_manifest(data_dir, manifest_path):
    #print("Creating manifest %s ..." % manifest_path)
    json_lines = []
    if os.path.isdir(data_dir):
        for file in os.listdir(data_dir):
            wav_filePath = os.path.join(data_dir, file)
            if any(wav_filePath.lower().endswith("." + ext) for ext in exts):
                Labels_filePath = wav_filePath.replace('.wav', '.txt')
                label_true = get_label_true_markSys(Labels_filePath)
                audio_data, samplerate = soundfile.read(wav_filePath)
                duration = float(len(audio_data)) / samplerate
                json_lines.append(
                    json.dumps({
                        'audio_filepath': wav_filePath,
                        'duration': duration,
                        'text': label_true
                    }))
    elif os.path.isfile(data_dir):
        wav_filePath = data_dir
        Labels_filePath = data_dir.replace('.wav', '.txt')
        label_true = get_label_true_markSys(Labels_filePath)
        audio_data, samplerate = soundfile.read(wav_filePath)
        duration = float(len(audio_data)) / samplerate
        json_lines.append(
            json.dumps({
                'audio_filepath': wav_filePath,
                'duration': duration,
                'text': label_true
            }))
    with codecs.open(manifest_path, 'w', 'utf-8') as out_file:
        for line in json_lines:
            out_file.write(line + '\n')


def file_2_mainfest(input_string):
    input_str = os.path.abspath(input_string)
    manifest_path = ""
    if os.path.isfile(input_str):
        if input_str.endswith(".wav"):
            manifest_path = input_str.replace(".wav",".manifest")
            create_manifest(input_str, manifest_path)
    elif os.path.isdir(input_str):
        manifest_path = input_str + ".manifest"
        create_manifest(input_str, manifest_path)
    else:
        pass
    return manifest_path


def txt_one2every(base_dir):
    txt_path = base_dir + ".txt"
    with open(txt_path, "r") as fr:
        for line in fr:
            line = line.strip('\r\n')
            filen, label = line.split('<------>')
            cur_txtfile = os.path.join(base_dir, filen + ".txt")
            with open(cur_txtfile, 'w') as fw:
                fw.write(rm_flags(label) + '\n')


def _levenshtein_distance(ref, hyp):
    m = len(ref)
    n = len(hyp)

    # special case
    if ref == hyp:
        return 0
    if m == 0:
        return n
    if n == 0:
        return m

    if m < n:
        ref, hyp = hyp, ref
        m, n = n, m

    # use O(min(m, n)) space
    distance = np.zeros((2, n + 1), dtype=np.int32)

    # initialize distance matrix
    for j in range(n + 1):
        distance[0][j] = j

    # calculate levenshtein distance
    for i in range(1, m + 1):
        prev_row_idx = (i - 1) % 2
        cur_row_idx = i % 2
        distance[cur_row_idx][0] = i
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                distance[cur_row_idx][j] = distance[prev_row_idx][j - 1]
            else:
                s_num = distance[prev_row_idx][j - 1] + 1
                i_num = distance[cur_row_idx][j - 1] + 1
                d_num = distance[prev_row_idx][j] + 1
                distance[cur_row_idx][j] = min(s_num, i_num, d_num)

    return distance[m % 2][n]


def char_errors(reference, hypothesis, ignore_case=False, remove_space=False):
    if ignore_case == True:
        reference = reference.lower()
        hypothesis = hypothesis.lower()

    join_char = ' '
    if remove_space == True:
        join_char = ''

    reference = join_char.join(filter(None, reference.split(' ')))
    hypothesis = join_char.join(filter(None, hypothesis.split(' ')))

    edit_distance = _levenshtein_distance(reference, hypothesis)
    return float(edit_distance), len(reference)


