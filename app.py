from flask import Flask, render_template, request
import os

# 크롤링 함수
from util.crawling import Search

# 워드클라우드 함수
from util.wordcloud import wordclouod_word
from util.wordcloud import wordclouod_word_index 

app = Flask(__name__)

@app.route('/')
def index():
    wordcloudword = wordclouod_word_index ('인공지능')    
    return render_template('index.html', word_list = wordcloudword, keyword = '인공지능')

@app.route('/search/')
def search():
    search = request.args.get('search')
    news = int(request.args.get('news'))
    Data_Collection = int(request.args.get('Data_Collection'))

    dir_path = f"./data/craw_data/{search}.csv"
    
    if os.path.isfile(dir_path) == False:
        Search(search, news, Data_Collection)        
    
    wordcloudword = wordclouod_word(search)

    return render_template('index.html', word_list = wordcloudword, keyword = search)

if __name__ == '__main__':    
    app.run()