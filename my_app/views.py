#これも追加
import requests
import re


#自動的に＋はいる。
from requests.compat import quote_plus

from django.shortcuts import render
from bs4 import BeautifulSoup
#pychamなら自動的にbs4入ってるらしい

#そしてデーターベースを加える
from . import models


# Create your views here.


#まずはサンディエゴで試す
BASE_CRAIGSLIST_URL = 'https://sandiego.craigslist.org/search/bbb?query={}'
#クエリは変わるので、上記記載

#imageの取り出し。少し特殊
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'



def home(request):
    return render(request, 'base.html')

def new_search(request):
    #データ取り出したい
    search = request.POST.get('search')#このgetはPOSTGETとは関係ない
    #以下で、データベースのSearchのところに加入。
    models.Search.objects.create(search=search)
    
    #＝＝＝＝＝＝以下はまさにハードコード
#    response = requests.get('https://sandiego.craigslist.org/search/bbb?query=python%20tutor&sort=rel')
#    data = response.text
#    print(data)
#    #＝＝＝＝＝＝＝＝
    #以下でフレキシブルに
    #print(quote_plus(search))
    #python+tutor
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li', {'class': 'result-row'})
#    #クラスのアンダーバーに注目
#    post_title = post_listings[0].find(class_= 'result-title').text
##    post_title = post_listings[0].find(class_= 'result-title')
##    
#    post_url = post_listings[0].find('a').get('href')
##    post_price = post_listings[0].find(class_='result-price').text
    
    #上記一気にやるよ
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_= 'result-title').text
        post_url = post.find('a').get('href')
        
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
            
        #イメージ、つまり写真を加える少し複雑。
        #画像で検索
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        
        final_postings.append((post_title, post_url, post_price, post_image_url))

#        final_postings.append((post_title, post_url, post_price))
        #        final_postings.append((post_title, post_url))

        
        
        
        
    
#
#        
#    print(post_title)
#    print(post_url)
#    #    print(post_price)

        



    
#    #タグ a と,class result-title。aはリンクのこと
#    post_titles = soup.find_all('a', {'class':'result-title'})
    #print(post_titles)
    #    print(post_titles[0])

    #    print(post_titles[0].text)
 #   print(post_titles[0].get('href'))

    #デベロッパーツールで、どのタイトルがどのクラスに属するかわかる。reslu_titleとか
    #print(data)
    
    
    
    
    
    #print(search)#この時点ではコンソールに出る
    #python tutor
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    
    return render(request, 'my_app/new_search.html', stuff_for_frontend)#ここで、new_search.htmlの書き換え

#pip freeze requirements
#ここでgit add git commitしてる