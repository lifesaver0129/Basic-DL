import re
import requests
from bs4 import BeautifulSoup
import time


def get_clothes():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/9.0.3497.100 Safari/537.36'
    }

    base_url = 'https://www.asos.com'
    contents_url = 'https://www.asos.com/women/'
    web_req = requests.get(contents_url, headers=headers)
    # web_req.encoding = 'UTF-8'
    web_text = web_req.text
    soup = BeautifulSoup(web_text, 'lxml')
    chapters = soup.find_all(class_='carousel__list js-carouselList')
    product_url = chapters[0].li.a["href"].replace('amp;', '')
    print (base_url + product_url)
    product_req = requests.get(base_url + product_url, headers=headers)
    product_text = product_req.text
    print(product_text)


# for j in range (page_start, page_end):
#     real_chap_num = finished_chapter + 10
#     with open("BossNovel"+str(real_chap_num)+"+.txt", "w") as f:
#         for _ in range (100):
#             try:
#                 chap_url = str(chapters[finished_chapter+1].a['href'])
#             except:
#                 exit()
#             web_req = requests.get(contents_url + chap_url)
#             web_req.encoding = 'GBK'
#             content = web_req.text.replace('<br />','').replace('<br>','').replace('()','')
#
#             content = re.compile('一秒(.*)免费读！！').sub('', content)
#             content = re.compile('书名(.*)?举报').sub('', content)
#             content = re.compile('201(.*)\?\?').sub('', content)
#
#             soup = BeautifulSoup(content, 'lxml')
#             heads = soup.find_all(class_ = 'readTitle')
#             divs = soup.find_all(class_ = 'panel-body')
#             try:
#                 f.write("\n")
#                 f.write(heads[0].get_text())
#                 f.write("\n----------------------\n")
#                 f.write(divs[0].get_text())
#                 finished_chapter += 1
#                 time.sleep(15)
#             except:
#                 pass

if __name__ == '__main__':
    get_clothes()
