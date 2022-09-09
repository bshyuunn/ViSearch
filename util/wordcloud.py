import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from eunjeon import Mecab

def wordcloud(input_data):
  data = pd.read_csv(r".\craw_data"'\\' + input_data + '.csv') 

  data = data.dropna()
  data = data.reset_index(drop=True)
  data = data.astype('string')

  tokenizer = Mecab()

  from nltk import FreqDist

  tokenized = []
  for i in range(len(data)):  
    tokenized.append(tokenizer.nouns(data["title"][i]))
    tokenized.append(tokenizer.nouns(data["text"][i]))      

  vocab = FreqDist(np.hstack(tokenized))
  
  vocab_sorted = sorted(vocab.items(), key= lambda x:x[1], reverse = True)

  word_num = len(vocab_sorted)
  for i in range(word_num):
    if len(vocab_sorted[word_num-i-1][0]) < 2:
      vocab_sorted.pop(word_num-i-1)    

  return vocab_sorted

def wordclouod_word(input_data):

  list = wordcloud(input_data)
  wordcolud_list = []

  for i in range(len(list)):
    wordcolud_list.append(list[i][0])

  return wordcolud_list

print(wordclouod_word("서울"))