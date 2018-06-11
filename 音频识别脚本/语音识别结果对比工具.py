import pandas as pd
import numpy as np
import os
from qq_try.音频结果分析.Statistics_actual_wav_recording import StatisticsWav


def outname(url):
    '''
    解析一个字段 如/home/qq2/2018-03-14/13002135628_1520997605_7725238_16.wav  变成 13002135628_1520997605_7725238_16.wav
    作为新的值
    :param url:
    :return:
    '''
    return url.strip().split("/")[-1]

def ReadIdentifyResults(filepath,Column_number=0):
    '''

    :param filepath:   文件路径,默认每列元素 以 ， 分割
    :param Column_number: 从Column_number 列开始读取   0 ~ n
    :return:
    '''
    read_data = pd.read_csv(filepath, header=None, sep=",")
    read_data = read_data.iloc[:, Column_number:]  # 所以行，只保留 第Column_number列以后的列元素
    name_pix = filepath
    columns_name = ['name', 'mean_{}'.format(name_pix), 'time_{}'.format(name_pix)]
    read_data.iloc[:,0] = read_data.iloc[:,0].apply(outname)
    read_data.columns = columns_name
    #print(filepath, read_data.iloc[:,1].count(), read_data.iloc[:,1].size, read_data.iloc[:,1].count()*100/read_data.iloc[:,1].size)
    #read_data.to_csv(filepath+".bak")
    return read_data

def merge_data(list_read_data, on="name",outpath="out.csv"):
    '''
    将 多个 有同一 列索引的 表数据 合并当同一个表中
    :param list_read_data:
    :param on:
    :param outpath:
    :return:
    '''
    if len(list_read_data) <=1:
        return list_read_data
    else:
        result_data = list_read_data[0]
        for node_data in list_read_data[1:]:
            result_data = pd.merge(result_data, node_data, on=on)
        if os.path.exists(outpath):
            os.remove(outpath)
        result_data.to_csv("out.csv",index=False)
        return result_data


def out_Analysis(read_data_df, read_wav):
    '''

    :param read_data_df: 读取识别结果的 txt文件
    :param file_data_df:读取实际的录音文件 ，分析录音文件的参数情况  read_wav
    :return:
    '''
    file_data_df = read_wav.wav_df

    print("可识别的内容中识别出内容的概率：", read_data_df.iloc[:,1].count()*100/read_data_df.iloc[:,1].size,
          "可以被识别，并且识别出内容的概率：",  read_data_df.iloc[:,1].count()*100/read_wav.total_wav_num)


if __name__ == "__main__":
    # from qq_try.音频结果分析.Statistics_actual_wav_recording import StatisticsWav
    # read_wav = StatisticsWav()

    tk_data = ReadIdentifyResults("tk.txt", 1)
    cc_data = ReadIdentifyResults("cc.txt")
    login_data = ReadIdentifyResults("login.txt")

    result_data = merge_data([tk_data, cc_data, login_data])
    print(result_data.head())
    print("tk",result_data.iloc[:,1].count()*100/result_data.iloc[:,1].size)
    print("cc",result_data.iloc[:,3].count()*100/result_data.iloc[:,1].size)
    print("login",result_data.iloc[:,5].count()*100/result_data.iloc[:,1].size)

    # out_Analysis(tk_data,read_wav)