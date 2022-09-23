# -*- coding: utf-8 -*-
from eunjeon import Mecab
import pandas as pd

import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

def find_sentence(find_word, data):    
    data = pd.read_csv(r".\.\data\craw_data"'\\' + data + '.csv')     

    tokenizer = Mecab()

    find = find_word
    answer = 'd'
    M = 0

    for i in range(len(data)):
        try:
            cnt = 0

            tokenized = []
            tokenized.append(tokenizer.nouns(data["text"][i]))

            for j in tokenized[0]:
                if j == find:
                    cnt += 1                              

            if cnt > M:            
                answer = data['text'][i]            
                M = cnt
        
        except:                
            continue
    
    tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
    model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')            
    text = answer.replace('\n', ' ')

    while True:   
        try:     
            raw_input_ids = tokenizer.encode(text)
            input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

            summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)            
            return tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

        except:
            length = len(text)
            length = int(length / 2)

            text_one = text[: (length - 20)]
            text_two = text[(length + 20): ]
            text = text_one + text_two            
            continue    
