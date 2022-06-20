import time
import requests
import pymongo
from bs4 import BeautifulSoup
import os, sys


os.chdir(os.getcwd())

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

dblist = myclient.list_database_names()
# dblist = myclient.database_names() 
if "news" in dblist:
    print("数据库已存在！")
else:
    mydb = myclient["news"]
    mytable = mydb["chinatimes"]

mydb = myclient["news"]
mytable = mydb["chinatimes"]

mytable.delete_many({})

page=1

while page<=5:
    chinatimes_URL="https://www.chinatimes.com/money/total?page="+str(page)+"&chdtv"
    response = requests.get(chinatimes_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    a=soup.select("h3>a")
    for url in a:
        response_inner=requests.get("https://www.chinatimes.com"+url['href'])
        soup_inner = BeautifulSoup(response_inner.text, "html.parser")
        title = soup_inner.find("h1").text
        article_time = soup_inner.find("time")['datetime']
        reporter = soup_inner.find("div", class_="author").text.replace("\n","")
        if reporter=="":
            reporter=reporter.select("a")[0].text.replace("\n","")
        content = soup_inner.find("div", class_="article-body")
        hash_tag = soup_inner.find("div", class_="article-hash-tag")
        content_txt=""
        tag_list=[]
        
        for tag in  hash_tag.select("a"):
            tag_list.append(tag.text)
        for p in content.select("p"):
            content_txt+=p.text
        
        news_data = {"resource": "中時財經總覽" , "title": title, "reporter": reporter,"news_time": article_time,"achieve_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"content":content_txt,"tag": tag_list,"url":"https://www.chinatimes.com"+url['href']}
        
        if mytable.count_documents(news_data)==0:
            mytable.insert_one(news_data) 
    page+=1

'''for x in mytable.find():
    print(x)'''


