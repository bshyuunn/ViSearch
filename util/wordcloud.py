import pandas as pd
import numpy as np
# from konlpy.tag import Mecab

from eunjeon import Mecab

input_data = input("분석할 데이터를 입력하세요 : ")
# 데이터 프레임에 저장

data = pd.read_csv(r".\craw_data"'\\' + input_data + '.csv') 

# print("전체 데이터 수 :", len(data))

# 데이터 프레임 수정
data = data.dropna()
data = data.reset_index(drop=True)
data = data.astype('string')

tokenizer = Mecab()

from nltk import FreqDist

tokenized = []
for i in range(len(data)):  
  tokenized.append(tokenizer.morphs(data["title"][i]))
  tokenized.append(tokenizer.morphs(data["text"][i]))      
  
vocab = FreqDist(np.hstack(tokenized))
# print("단어 집합의 크기 : {}".format(len(vocab)))
vocab_sorted = sorted(vocab.items(), key= lambda x:x[1], reverse = True)

word_num = len(vocab_sorted)
for i in range(word_num):
  if len(vocab_sorted[word_num-i-1][0]) < 2:
    vocab_sorted.pop(word_num-i-1)

print(vocab_sorted[0])