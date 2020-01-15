from bs4 import BeautifulSoup
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor


def get_page(url):
    response = requests.get(url=url,headers=headers).text
    soup = BeautifulSoup(response,'lxml')
    # body > div.main > div.content > div.pagenavi > a:nth-child(7) > span
    total_num = soup.select('body > div.main > div.content > div.pagenavi > a:nth-child(7) > span')
    total_num = total_num[0].string
    image_list=[]
    print('运行到3')
    time.sleep(5)#读取太多次会返回Too Many Request异常
    for i in range(int(total_num)):
        image_url = url+'/'+str(i+1)
        html = requests.get(image_url,headers=headers).content
        src = BeautifulSoup(html,'lxml')
        src = src.find('img').get('src')
        image_list.append(src)
        time.sleep(0.5)
    return image_list

def getUrl(target):
    #先获取全部的li 然后得到每个li的title和url
    headers={'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
    }
    response = requests.get(url=target,headers=headers).text
    soup = BeautifulSoup(response,'lxml')
    girl_list = soup.find(class_="postlist").find_all('li')
    print('运行到1')
    with ThreadPoolExecutor(3) as t:
        for girl in girl_list:
            if girl.get('class')=='box':
                continue
            title = girl.find('span').find('a').text
            print(title)
            url = girl.find('span').find('a').get('href')
            print('运行到2')
            image_list = get_page(url)
            t.submit(download_Pic,title,image_list)
            # download_Pic(title,image_list)
    
def download_Pic(title, image_list):
    # 新建文件夹
    dirname = title
    os.mkdir(dirname)
    j = 1
    # 下载图片
    for item in image_list:
        filename = '%s/%s.jpg' % (dirname,str(j))
        print('downloading....%s : NO.%s' % (title,str(j)))
        print(item)
        with open(filename, 'wb') as f:
            img = requests.get(item,headers=headers).content
            f.write(img)
        j+=1        

def main():
    getUrl('https://www.mzitu.com/')

if __name__ == "__main__":
    headers={'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
    }
    os.mkdir('result_multiThread')
    os.chdir('result_multiThread')
    main()


    