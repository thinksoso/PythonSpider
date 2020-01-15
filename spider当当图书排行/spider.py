import requests
import re


def getUrl(page):
    urllist=[]
    for i in range(int(page)+1):
        if i == 0:
            continue
        url='http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-'+str(i)
        urllist.append(url)
    return urllist

def getPage(urllist):
    i=0
    for url in urllist:
        i=i+1
        print("正在爬取第%d页"%(i))
        html=requests.get(url).text
        for content in parse_result(html):
            write_item_to_file(content)

def parse_result(html):
   pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
   items = re.findall(pattern,html)
   # yield是生成器表示，每次返回一次右边的值，并保存位置，下一次继续从上一次的位置开始
   for item in items:
       yield {
           'range': item[0],
           'iamge': item[1],
           'title': item[2],
           'recommend': item[3],
           'author': item[4],
           'times': item[5],
           'price': item[6]
       }

def write_item_to_file(item):
   print('开始写入数据 ====> ' + str(item))
   with open('book.txt', 'a', encoding='UTF-8') as f:
       f.write(str(item))
       f.write('\n')
       f.close()
def main():
    page=input('请输入要爬取的页数')
    urllist=getUrl(page)
    print(urllist)
    getPage(urllist)
    

if __name__ == "__main__":
    main()