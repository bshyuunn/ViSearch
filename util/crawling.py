from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import pandas as pd

# 데이터프레임 선언
craw_df = pd.DataFrame({"title" : [],
                   "text" : []}
                   )

# title 링크 저장
href_data = []

# 검색어 결과 제목 및 링크 크로링하기
def craw_title_href(num, news, search):
    global craw_df
    global href_data    

    try:

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome('./util/chromedriver', options=options)

        url = 'https://www.google.com/search?q='
        url += search
            
        # 뉴스 페이지에서 검색
        if news == 1:        
            url += '&source=lmns&tbm=nws' 

            url += '&start='
            url += str(num) + str(0)
            
            driver.get(url)
            
            html = driver.page_source
            soup = BeautifulSoup(html)
            
            title = soup.select('.xuvV6b.BGxR7d')             
            
            for i in title:      
                craw_df = craw_df.append({'title' : i.select_one('.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d').text}, ignore_index=True)
                href_data.append(i.a.attrs['href'])

            driver.close()
        
        # 전체 페이지에서 검색
        else:        
            url += '&start='
            url += str(num) + str(0)
            
            driver.get(url)
            
            html = driver.page_source
            soup = BeautifulSoup(html)
            
            title = soup.select('.kvH3mc.BToiNc.UK95Uc')  
                    
            
            for i in title:      
                craw_df = craw_df.append({'title' : i.select_one('.LC20lb.MBeuO.DKV0Md').text}, ignore_index=True)
                href_data.append(i.a.attrs['href'])

            driver.close()
    except: 
        return 0


# 수집한 링크의 본문 글까지 크롤링하기
def additional_craw(href_data):
    global craw_df
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")    
    
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome('./util/chromedriver', options=options)

    for i in range(len(href_data)):
        try:
            url = href_data[i]
            driver.get(url)

            html = driver.page_source
            soup = BeautifulSoup(html)

            text = soup.select('p')
            temp = ''

            for j in text:
                temp += j.text
            craw_df.loc[i, 'text'] = temp    
            
            print("=======================================")
            print('2차 크롤링 중', f'{i+1}/{len(href_data)}' )
            print("=======================================")   
        except:
            continue

    print("=======================================")
    print('2차 크롤링 완료!')
    print("=======================================")

# Search(검색 키워드, news에서 검색 시 1 아닐 시 0, 데이터 수집 양 적게 : 1 보통 : 2 많이 : 3)
def Search(search, news, Data_Collection):
    global craw_df
    global href_data  

    # 데이터프레임 선언
    craw_df = pd.DataFrame({"title" : [],
                    "text" : []}
                    )

    # title 링크 저장
    href_data = []


    
    if Data_Collection == 1:
        Data_Collection = 2
    elif Data_Collection == 2:
        Data_Collection = 5
    elif Data_Collection == 3:
        Data_Collection = 10  

    # 페이지 10개 크롤링
    for i in range(Data_Collection):
        try:

            craw_title_href(i, news, search)
            print("=======================================")
            print('1차 크롤링 중', f'{i+1}/{Data_Collection}' )
            print("=======================================")

        except:
            continue

    print("=======================================")
    print('1차 크롤링 완료!')
    print("=======================================")

    additional_craw(href_data)

    file_name = search
    craw_df.to_csv(f'./data/craw_data/{file_name}.csv', encoding='utf-8')
    


# # 검색어 입력받기
# search = input('검색어를 입력하시요 : ')
# news = int(input("\n전체 페이지 검색 : 0 \n뉴스 페이지에서 검색 : 1\n입력 : "))
# Data_Collection = int(input("\n적게 : 1 \n보통 : 2 \n많이 : 3 \n입력 : "))

# Search(search, news, Data_Collection)