# 대사와 설명, 설명과 등장인물이 같은 형식으로 등장, 따라서 전후 관계를 이용하고, 예외는 직접 확인함
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
index = 50                                          # 태깅할 영화 선택
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
script = script[366:]
script = script.split("\n")
#script = list(filter(lambda x: x!= '', script)) # 공백 제거



#태깅

# 정규식


situation_line_re = re.compile(' {10}')                # 상황설명 1 대사3
person_command_re = re.compile(' {25}')                # 등장인물 2  지시4
#line_re = re.compile(' {11}')                     # 대사 3
#command_re = re.compile(' {25}')                  # 지시 4
alphabet_re = re.compile('[A-Z]+ *[0-9]*')
number_re = re.compile('[0-9]+')
temp_re = re.compile('[:]+')
temp1_re = re.compile('A8')
temp2_re = re.compile('ANGLE')
temp3_re = re.compile('SHOT')



#in_re = re.compile('INT. ')
#out_re = re.compile('EXT. ')                # 장소(내부/외부) 5
#time_re = re.compile(' ')                          # 시간 6
#era_re = re.compile(' ')                           # 시대 7
#                                                   # 그외 0
not_re = re.compile(' *[\d]]+')
#------------------------------------------------------------------------------
sentence_cnt = 0    # Data Frame의 index로 사용
sentence_label = 0  #대사인지확인
sentence_temp1 = "" #설명
sentence_temp2 = "" #대사

is_time = False     # 시간에 관한 데이터가 장소에 대한 data 보다 나중에 입력되지 않게 하기위해 사용

# 태깅 진행

for sc in script:
    if len(sc.strip()) == 0:
        sentence_label = 0
    else:
        if person_command_re.search(sc):
            if alphabet_re.search(sc) and not temp1_re.search(sc):
                if sc.strip().rfind(" ") != -1 and number_re.search(sc.strip()[sc.strip().rfind(" "):]) :
                    sc = sc.strip()[:sc.strip().rfind(" ")]
                if sc.strip()[0] == '(':
                    df.loc[sentence_cnt, 'sentence'] = sc.strip()
                    df.loc[sentence_cnt, 'label'] = 4
                    sentence_label = 4
                    sentence_cnt += 1
                elif temp_re.search(sc) or re.findall("SHOT",str(sc)) or re.findall("ANGLE",str(sc)) or sc.strip() in {"Â€¢", "FADE IN", "FADE OUT"} :
                    df.loc[sentence_cnt, 'sentence'] = sc.strip()
                    df.loc[sentence_cnt, 'label'] = 1
                    sentence_label = 1
                    sentence_cnt += 1
                elif sc.strip() in {"LAWSON", "WIFE", "JENNY", "MATRIX", "DIAZ", "BENNETT", "ARIUS", "KIRBY", "SOLDIER", "HENRIQUES", "STEWARDESS", "CINDY", "I'LLTR IX", "SULLY", "FORRESTAL", "COOKE", "JACKSON"}:
                    df.loc[sentence_cnt, 'sentence'] = sc.strip()
                    df.loc[sentence_cnt, 'label'] = 2
                    sentence_label = 2
                    sentence_cnt += 1
                else:
                    df.loc[sentence_cnt, 'sentence'] = sc.strip()
                    df.loc[sentence_cnt, 'label'] = 24
                    sentence_label = 24
                    sentence_cnt += 1
        elif situation_line_re.search(sc):
            if sentence_label in {0, 1}:
                if re.findall("INT. ", str(sc)) or re.findall("EXT. ", str(sc)):
                    sc = sc.strip()[: sc.strip().rfind(" ")]
                    df.loc[sentence_cnt, 'sentence'] = sc[0:4]
                    df.loc[sentence_cnt, 'label'] = 5
                    sentence_label = 56
                    sentence_cnt += 1

                    sc_arr = sc.strip()[5:].split(' - ')
                    for idx, sc_elem in enumerate(sc_arr):
                        df.loc[sentence_cnt, 'sentence'] = sc_elem.strip()
                        if idx == len(sc_arr) - 1:
                            df.loc[sentence_cnt, 'label'] = 6
                            sentence_cnt += 1
                        else:
                            df.loc[sentence_cnt, 'label'] = 5
                            sentence_cnt += 1
                else:
                    sentence_label = 1
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
            elif sentence_label in {2, 24, 3, 4}:
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
            else:
                df.loc[sentence_cnt, 'sentence'] = sc.strip()
                df.loc[sentence_cnt, 'label'] = 0
                sentence_label = 0
                sentence_cnt += 1
        else:
            df.loc[sentence_cnt, 'sentence'] = sc.strip()
            df.loc[sentence_cnt, 'label'] = 0
            sentence_label = 0
            sentence_cnt += 1



# 결과
# df.loc[sentence_cnt, 'label'] = 0
# df = df.sort_index()
#
# for x in range(sentence_cnt):
#     if df.loc[x, 'label'] == 0 or ' ':
#         print(df.loc[x, 'sentence'], "                  index of data >> ", x)

df.to_csv(tagging_link, index = False)
