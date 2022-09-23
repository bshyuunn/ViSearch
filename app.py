# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import os

# 크롤링 함수
from util.crawling import Search

# 워드클라우드 함수
from util.wordcloud import wordclouod_word
from util.wordcloud import wordclouod_word_index 

# 문장 요약
from util.find_sentence import find_sentence

app = Flask(__name__)

@app.route('/')
def index():
    wordcloudword = wordclouod_word_index('인공지능')            
    search = '인공지능'

    summary_sentence = '옆의 요약하고 싶은 키워드를 누르세요!'

    try:                
        summary = request.args.get('summary') 
        summary_sentence = find_sentence(summary, search)    

    except:
        summary_sentence = '옆의 요약하고 싶은 키워드를 누르세요!'  
    
    return render_template('index.html', word_list = wordcloudword, keyword = search, summary = summary_sentence) 

@app.route('/search/')
def search():

    search = request.args.get('search')
    summary = request.args.get('summary') 
    
    try:        
        news = int(request.args.get('news'))    
        Data_Collection = int(request.args.get('Data_Collection'))                   
    except:
        pass

    dir_path = f"./data/craw_data/{search}.csv"
    
    if os.path.isfile(dir_path) == False:
        Search(search, news, Data_Collection)        
    
    wordcloudword = wordclouod_word(search)

    try:
        search_word = search
        find_word = summary

        summary_sentence = find_sentence(find_word, search_word)                                    

    except:
        summary_sentence = '옆의 요약하고 싶은 키워드를 누르세요!'        

    return render_template('index.html', word_list = wordcloudword, keyword = search, summary = summary_sentence)

if __name__ == '__main__':    
    app.run()