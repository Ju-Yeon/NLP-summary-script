#대문자 대본내용 지시사항(4)으로 간주, 설명(1)과 조금 혼동우려있음(확인해볼 것)

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
index = 49                                          # 태깅할 영화 선택
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
script = script[203:]
script = script.split("\n")
script = list(filter(lambda x: x!= '', script)) # 공백 제거




#태깅

# 정규식

sentence_re = re.compile('[a-zA-Z]+')
situation_re = re.compile(' {10}')                # 상황설명 1
person_re = re.compile(' {26}')                   # 등장인물 2
line_re = re.compile(' {11}')                     # 대사 3
command_re = re.compile(' {25}')                  # 지시 4
not_command_re = re.compile('[a-z]+')


in_re = re.compile('INT. ')
out_re = re.compile('EXT. ')                # 장소(내부/외부) 5
#time_re = re.compile(' ')                          # 시간 6
#era_re = re.compile(' ')                           # 시대 7
#                                                   # 그외 0
not_re = re.compile(' *[\d]]+')
#------------------------------------------------------------------------------
sentence_cnt = 0    # Data Frame의 index로 사용
sentence_temp1 = "" #설명
sentence_temp2 = "" #대사

is_time = False     # 시간에 관한 데이터가 장소에 대한 data 보다 나중에 입력되지 않게 하기위해 사용

# 태깅 진행

for sc in script:
    if sentence_re.search(sc):
        if person_re.search(sc):
            if sc.strip()[0] == '(':
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 4
                sentence_cnt += 1
            else:
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 2
                sentence_cnt += 1

        elif command_re.search(sc):
            df.loc[sentence_cnt, 'sentence'] = sc.strip()
            df.loc[sentence_cnt, 'label'] = 4
            sentence_cnt += 1

        elif line_re.search(sc):
            if sc.rfind('.') != -1:
                sentence_temp2 += " " + sc.strip()[0:sc.strip().rfind('.') + 1]
                df.loc[sentence_cnt, 'sentence'] = sentence_temp2.strip()
                df.loc[sentence_cnt, 'label'] = 3
                sentence_cnt += 1
                sentence_temp2 = sc[sc.rfind('.') + 1:]
            elif sc.rfind('?') != -1:
                sentence_temp2 += " " + sc.strip()[0:sc.strip().rfind('?') + 1]
                df.loc[sentence_cnt, 'sentence'] = sentence_temp2.strip()
                df.loc[sentence_cnt, 'label'] = 3
                sentence_cnt += 1
                sentence_temp2 = sc[sc.rfind('?') + 1:]
            elif sc.rfind('!') != -1:
                sentence_temp2 += " " + sc.strip()[0:sc.strip().rfind('!') + 1]
                df.loc[sentence_cnt, 'sentence'] = sentence_temp2.strip()
                df.loc[sentence_cnt, 'label'] = 3
                sentence_cnt += 1
                sentence_temp2 = sc[sc.rfind('!') + 1:]
            else:
                sentence_temp2 += " " + sc.strip()

        elif situation_re.search(sc):
            if in_re.search(sc) or out_re.search(sc):
                df.loc[sentence_cnt, 'sentence'] = sc.strip()[0:4]
                df.loc[sentence_cnt, 'label'] = 5
                sentence_cnt += 1

                sc_arr = sc.strip()[5:].split(' - ')

                for idx, sc_elem in enumerate(sc_arr):
                    df.loc[sentence_cnt, 'sentence'] = sc_elem.strip()
                    if idx == len(sc_arr)-1:
                        df.loc[sentence_cnt, 'label'] = 6
                    else:
                        df.loc[sentence_cnt, 'label'] = 5
                    sentence_cnt += 1
            else:
                if sentence_temp1 != "" or not_command_re.search(sc):
                    if sc.rfind('.') != -1:
                        sentence_temp1 += " " + sc.strip()[0:sc.strip().rfind('.') + 1]
                        df.loc[sentence_cnt, 'sentence'] = sentence_temp1.strip()
                        df.loc[sentence_cnt, 'label'] = 1
                        sentence_cnt += 1
                        sentence_temp1 = sc[sc.rfind('.') + 1:]
                    elif sc.rfind(':') != -1:
                        sentence_temp1 += " " + sc.strip()[0:sc.strip().rfind(':') + 1]
                        df.loc[sentence_cnt, 'sentence'] = sentence_temp1.strip()
                        df.loc[sentence_cnt, 'label'] = 1
                        sentence_cnt += 1
                        sentence_temp1 = sc[sc.rfind(':') + 1:]
                    else:
                        sentence_temp1 += " " + sc.strip()

                else:
                    df.loc[sentence_cnt, 'sentence'] = sc.strip()
                    df.loc[sentence_cnt, 'label'] = 4
                    sentence_cnt += 1

        else:
            df.loc[sentence_cnt, 'sentence'] = sc.strip()
            df.loc[sentence_cnt, 'label'] = 0
            sentence_cnt += 1

    # else:
    #     df.loc[sentence_cnt, 'sentence'] = sc.strip()
    #     df.loc[sentence_cnt, 'label'] = -1
    #     sentence_cnt += 1





# # 결과
# # df.loc[sentence_cnt, 'label'] = 0
# # df = df.sort_index()
# #
# # for x in range(sentence_cnt):
# #     if df.loc[x, 'label'] == 0 or ' ':
# #         print(df.loc[x, 'sentence'], "                  index of data >> ", x)
#
df.to_csv(tagging_link, index = False)
