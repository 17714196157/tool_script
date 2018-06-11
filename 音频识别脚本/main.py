from jlhs.jths_asr_8 import recog_single as jths8_recog_single
from jlhs.jths_asr_16 import recog_single as jths16_recog_single
import os
import pandas as pd

BasePath = os.path.dirname(os.path.abspath(__file__))
input_war_folder_path = os.path.join(BasePath, 'input')
input_war_folder_path_8k = os.path.join(input_war_folder_path, '8k')
input_war_folder_path_16k = os.path.join(input_war_folder_path, '16k')

list_wav_name = os.listdir(input_war_folder_path_8k)
# print(list_wav_name)

df = pd.DataFrame(list_wav_name,columns=['wav_name'])
print(df)

df['jths8'] = ""
for wav_name in list_wav_name:
    path_war = os.path.join(input_war_folder_path_8k, wav_name)
    # print(path_war)
    RecognitionResults = jths8_recog_single(path_war)
    print(path_war, RecognitionResults[1])

df['jths16'] = ""
for wav_name in list_wav_name:
    path_war = os.path.join(input_war_folder_path_16k, wav_name)
    # print(path_war)
    RecognitionResults = jths16_recog_single(path_war)
    print(path_war, RecognitionResults[1])

