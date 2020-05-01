# 장소, 시간, 인물, 지시사항은 임의의 순서로 나오기 때문에, 56으로 태그 되있는 것은 다시 확인해야함

# Tagging 방법

# **태깅** 요소
# 상황설명 : 1<br>
# 등장인물 : 2<br>
# 대사 : 3<br>
# 지시사항/감정 : 4<br>
# 장소 : 5<br>
# 시간 : 6<br>
# 시대 : 7<br>
# 그 외 : 0<br>


import pandas as pd
import numpy as np
import re


link = "./movie_Action.csv"                         # movie_Action.csv load
index = 48                                          # 태깅할 영화 선택
data = pd.read_csv(link)                            # movie_Action data의 Data Frame 생성
imdbID = data.loc[index, 'imdb_id']                 # imdb id 추출

tagging_link = "./" + imdbID + ".csv"               # tagged script 저장 위치
txt_link = "./" + imdbID + ".txt"


df = pd.DataFrame(columns=["sentence", "label"])    # tagged scrpt의 Data Frame 생성



# 사용할 script를 txt 파일로 변환 및 로드
temp_prepro =(data.loc[index, 'script'])


# txt 파일로 저장
with open(txt_link, 'w') as f:
    for x in temp_prepro:
        f.write(x)


# txt 파일 불러와서 list로 저장
script = []
with open(txt_link, 'r') as f:
    lines = f.readlines()
    for line in lines:
        script.append(line)


#대본 전처리

# script 조작
script = (data.loc[index, 'script'])
script = script[737:]
script = script.split("\n")
script = list(filter(lambda x: x!= '', script)) # 공백 제거


#태깅

# 정규식

novalue_re = re.compile(' {50}')
situation_re = re.compile(' {4,5}')                # 상황설명 1
person_re = re.compile(' {28,32}')                 # 등장인물 2
line_re = re.compile(' {14,18}')                   # 대사 3
command_re = re.compile('[(]{1}')                  # 지시 4


in_re = re.compile('INT.')
out_re = re.compile('EXT.')
inout_re = re.compile('INT./EXT.')                  # 장소(내부/외부) 5
time_re = re.compile(' - [A-Z]+$')                  # 시간 6
#era_re = re.compile(' ')                           # 시대 7
#                                                   # 그외 0
not_re = re.compile(' *[\d]]+')
#------------------------------------------------------------------------------
sentence_cnt = 0    # Data Frame의 index로 사용
sentence_temp = ""
is_time = False     # 시간에 관한 데이터가 장소에 대한 data 보다 나중에 입력되지 않게 하기위해 사용

# 태깅 진행

for sc in script:
    if sc[0] != ' ':
        sc = sc[sc.find(' '):sc.rfind(' ')]
        if inout_re.search(sc):
            df.loc[sentence_cnt, 'sentence'] = 'INT./EXT.'
            df.loc[sentence_cnt, 'label'] = 5
            sentence_cnt += 1
            sc = sc[10:]
        elif in_re.search(sc):
            df.loc[sentence_cnt, 'sentence'] = 'INT.'
            df.loc[sentence_cnt, 'label'] = 5
            sentence_cnt += 1
            sc = sc[5:]
        elif out_re.search(sc):
            df.loc[sentence_cnt, 'sentence'] = 'EXT.'
            df.loc[sentence_cnt, 'label'] = 5
            sentence_cnt += 1
            sc = sc[5:]

        sc_arr = sc.split(' - ')
        for sc in sc_arr:
            if sc.strip() in ['LATER', 'DAY', 'NIGHT', 'MORNING', 'MOMENTS LATER', 'DAY/NIGHT', 'ANOTHER DAY', 'FEW MOMENTS LATER', 'BEAT LATER']:
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 6
                sentence_cnt += 1
            elif sc.strip() == 'CONTINUED:':
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 1
                sentence_cnt += 1
            else:
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 56
                sentence_cnt += 1
    else:
        if novalue_re.search(sc):
            continue
        elif person_re.search(sc):
            df.loc[sentence_cnt, 'sentence'] = sc.strip()
            df.loc[sentence_cnt, 'label'] = 2
            sentence_cnt += 1
        elif line_re.search(sc):
            if command_re.search(sc):
                df.loc[sentence_cnt, 'sentence'] = sc.strip()[1:-1]
                df.loc[sentence_cnt, 'label'] = 4
                sentence_cnt += 1
            else:
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 3
                sentence_cnt += 1
        elif situation_re.search(sc):
            if sc.rfind('.') != -1:
                sentence_temp += " " + sc.strip()[0:sc.strip().rfind('.') + 1]
                df.loc[sentence_cnt, 'sentence'] = sentence_temp.strip()
                df.loc[sentence_cnt, 'label'] = 1
                sentence_cnt += 1
                sentence_temp = sc[sc.rfind('.') + 1:]
            elif sc.rfind(':') != -1:
                sentence_temp += " " + sc.strip()[0:sc.strip().rfind(':') + 1]
                df.loc[sentence_cnt, 'sentence'] = sentence_temp.strip()
                df.loc[sentence_cnt, 'label'] = 1
                sentence_cnt += 1
                sentence_temp = sc[sc.rfind(':') + 1:]

            else:
                sentence_temp += " " + sc.strip()
        else:
            df.loc[sentence_cnt, 'sentence'] = sc.strip()
            df.loc[sentence_cnt, 'label'] = 0
            sentence_cnt += 1





# 결과
# df.loc[sentence_cnt, 'label'] = 0
# df = df.sort_index()
#
# for x in range(sentence_cnt):
#     if df.loc[x, 'label'] == 0 or ' ':
#         print(df.loc[x, 'sentence'], "                  index of data >> ", x)

df.to_csv(tagging_link, index = False)
