from flask import Flask, render_template, request

# 크롤링 함수
from util.crawling import Search

# 워드클라우드 함수
from util.wordcloud import wordclouod_word

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/')
def search():
    search = request.args.get('search')
    news = int(request.args.get('news'))
    Data_Collection = int(request.args.get('Data_Collection'))
    
    Search(search, news, Data_Collection)        
    wordcloudword = wordclouod_word(search)    

    return render_template('search.html', word_list = wordcloudword)

if __name__ == '__main__':    
    app.run()