from bs4 import BeautifulSoup
import requests

def  getUrl(page):
    urlList=[]
    for i in range(page):
        url='https://movie.douban.com/top250?start='+str(i*25)+'&filter='
        urlList.append(url)
    print(urlList)
    return urlList

def getPage(urlList):
    for url in urlList:
        print("url"+url)
        try:
            headers={
            'Host': 'movie.douban.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
            }
            response = requests.get(url,headers=headers)
            # print(response.status_code)
            if response.status_code == 200:
                response=response.text
                print("成功")
        except requests.RequestException:
            return None
        
        # print("response:"+response)
        soup=BeautifulSoup(response,'lxml')
        print(soup)
        # //*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1] //*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]/text()[1]
        item_list=soup.find(class_='grid_view').find_all(name='li')
        for item in item_list:
            item_info=item.find(class_='info')
            yield {
                'name':item_info.find(class_='title').string,
                'img':item.find(class_='pic').find('img').get('src'),
                'index':item.find(class_='').string,
                'star':item.find(class_='rating_num').text,
                'comment':item.find(class_='inq').text,
                'director':item.find(class_='bd').find('p').text
            }

def write_to_file(item):
    film='第'+item['index']+'名 '+'电影名:'+item['name']+' 图片:'+item['img']+'  星级:'+item['star']+'  评论:'+item['comment']
    f=open('top250.txt','a',encoding='UTF-8')
    f.write(film)
    f.write('\n')
    f.close()
    
def main():
    page=10
    url_list=getUrl(page)
    for item in getPage(url_list):
        write_to_file(item)

if __name__ == "__main__":
    main()