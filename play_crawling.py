
# https://jmoon.co.kr/241

#https://mokeya.tistory.com/156
url='https://play.google.com/store/apps/details?id=xyz.whatssub.application'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
options = Options()
options.add_argument('--kiosk')

SCROLL_PAUSE_TIME =2
SCROOL_TIMES = 4 # 4번 스크롤 후 더보기 버튼 생성되기에 4
CLICK_PAUSE_TIME = 2

#리뷰 전체 보기 버튼 클릭 함수 정의
element = "button.VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.QDwDD.mN1ivc.VxpoF[aria-label='평가 및 리뷰 자세히 알아보기']"

def click_element(driver):
    click_target =driver.find_element(by=By.CSS_SELECTOR, value=element)
    click_target.click()
    time.sleep(3)

driverPath='C:\chromedriver' #크롬드라이브 설치된 경로, 해당 파일의 저장경로와 동일하면 그냥 파일명만
driver=webdriver.Chrome(driverPath) #Open Chrome
driver.get(url)
time.sleep(3)
click_element(driver) #브라우저 열어서 -> 평가 및 리뷰 전체보기 버튼 클릭

############################################3
#여기서 수작업으로 리뷰 밑에까지 보이게 놔야 함..
#############################################3
title = driver.find_element(by=By.CSS_SELECTOR, value='h5,xzVNx').text

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.findAll('div', {'class':'RHo1pe'})
print(title)
print(len(content))

item_list=[
    'iXRFPc', #별점
    'h3YV2d', #리뷰
    'AJTPPZc' # 리뷰 동조자 수
]
#수집 대상 요소를 칼람으로 하는 빈 list생성
tmp_list = []
print(len(content))

for i in range(len(content)):
    try:
        item1 = content[i].find('div', {'class': item_list[1]}).text
    except:
        item1 =''

    try:
        item2 = content[i].find('div', {'class': item_list[0]})['aria-label']
    except:
        item2=''
    try:
        item3 = content[i].find('div', {'class': item_list[2]}).text
    except:
        item3 = str(0)
    tmp_list.append([item1, item2, item3])

import pandas as pd
from pandas import DataFrame
from datetime import datetime

# 위 과정의 결과물은 list형태이기 때문에 이를 dataframe으로 변형
# DF로 변형하면서 칼럼명도 변경

result_df =DataFrame(tmp_list, columns=['리뷰내용',
                                        '별점',
                                        '리뷰동조자수'])
result_df.head()

tmp = result_df.copy()

tmp['별점'] = tmp['별점'].apply(lambda x: x[5:])

import re
m = re.compile('[0-9][\.0-9]*') #정규표현식 사용

tmp['별점'] = tmp['별점'].apply(lambda x : m.findall(x)[0])
tmp['리뷰동조자수']=tmp['리뷰동조자수'].apply(lambda x: m.findall(x)[0])
tmp.head(3)

#엑셀 파일로 저장
date = datetime.today().strftime('%Y-%m-%d')
tmp.to_excel("("+date+")_왓섭.xlsx", index=False)
