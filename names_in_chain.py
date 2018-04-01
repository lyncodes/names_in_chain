import requests
import re
import pypinyin as py
import numpy as np
import pandas as pd


url='http://www.360doc.com/content/16/0419/10/877149_551849520.shtml'
r = requests.get(url)
r.encoding = 'utf-8'

s_name = re.findall('[\u4e00-\u9fa5]{1,3}市', r.text)
s_name = list(set(s_name))
shi = []
for i in s_name:
    shi.append(i[:-1])
shi_removed = shi.remove('中国省')
shi_removed = shi.remove('国各省')
shi_removed = shi.remove('县级')
shi_removed = shi.remove('辖地级')
shi_removed = shi.remove('县个级')
shi_removed = shi.remove('全国省')

x_name = re.findall('[\u4e00-\u9fa5]{1,3}县', r.text)
x_name = list(set(x_name))
xian = []
for i in x_name:
	xian.append(i[:-1])

q_name = re.findall('[\u4e00-\u9fa5]{2,3}区', r.text)
q_name = list(set(q_name))
qu = []
for i in q_name:
	qu.append(i[:-1])
qu.remove('国地名')
qu.remove('各省市')
qu.remove('个市辖')
qu.remove('族自治')
qu.remove('省行政')
qu.remove('省市县')
qu.remove('个地')
qu.remove('尔自治')
qu.remove('别行政')
qu.remove('藏自治')
qu.remove('古自治')
qu.remove('万山特')
qu.remove('六枝特')

qu.append('香港')
qu.append('西藏')
qu.append('澳门')
qu.append('新疆')
qu.append('宁夏')
qu.append('广西')

all_name = list(set(shi+xian+qu))
all_name = np.reshape(all_name,-1)

all_pinyin = py.pinyin(all_name)
all_pinyin = np.reshape(all_pinyin,-1)

word_length = []
for i in all_name:
    word_length.append(len(i))
word_length = np.array(word_length)

count = 0
end_position = []
for i in word_length:
    count+=i
    end_position.append(count)
end_position = np.array(end_position)

front_position = [m - n + 1 for m,n in zip(end_position,word_length)] 
front_position = np.array(front_position)

front_pinyin = []
for i in front_position:
    front_pinyin.append(all_pinyin[i - 1])
front_pinyin = np.reshape(front_pinyin,-1)


end_pinyin = []
for i in end_position:
    end_pinyin.append(all_pinyin[i - 1])
end_pinyin = np.reshape(end_pinyin,-1)


df = pd.DataFrame(all_name,np.arange(len(all_name)))

df[1] = front_pinyin
df[2] = end_pinyin
df.columns = ["地名","头拼音","尾拼音"]

place_list = df['地名'].tolist()
head_pinyin_list = df['头拼音'].tolist()
end_pinyin_list = df['尾拼音'].tolist()


get_name = input("请输入地名（比如北京）：")
while get_name:
    if get_name == 'QUIT':
        exit()
    else:
        if get_name in place_list:
            print("存在这个地名\n")
            if end_pinyin_list[place_list.index(get_name)] in head_pinyin_list:
                print('并且存在后继地名，后继城市有如下：\n')
                place_count = 0
                for i in place_list:
                    if end_pinyin_list[place_list.index(get_name)] == head_pinyin_list[place_list.index(i)]:
                        place_count+=1
                        print(place_count,i)
                print('选择一个地名来继续地名接龙,输入其中一个可能的地名：')
                get_name = input('哪一个地名你选择？退出请输入QUIT。')
            else:
                print('但是不存在后继地名,请换一个地名重新开始。')
                get_name = input()
        else:
            print("不存在这个地名")
            print('但是不存在后继地名,请换一个地名重新开始。')
            get_name = input()

