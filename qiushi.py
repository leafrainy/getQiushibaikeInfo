# -*- coding: utf-8 -*-
#一键获取糗事百科昵称头像入库
#leafrainy
#leafrainy.cc
from bs4 import BeautifulSoup as bs
import requests as r
import pymysql
import time


#想要抓取的页数，抓取1-13页就写14
endPage = 14

#数据库连接
conn = pymysql.connect(host="localhost", user="dev",password="dev",database="dev",charset="utf8")


#写入数据库
def insertData(name,headimg,conn=conn):
    cursor = conn.cursor()

    
    sql = "SELECT * FROM head WHERE name=%s or headimg=%s;"
    try:
        isExit = cursor.execute(sql,(name,headimg))
        if(isExit):
            print(name+"已存在")
            #exit()
        else:
            sql2="insert into head (name,headimg) VALUE (%s,%s);"
            try:
                cursor.execute(sql2,(name,headimg))
                print(name+"--插入成功")
                #exit()
            except Exception as ee:
                conn.rollback()
                print(name+"--数据写入失败，有错误，已回滚")

    except Exception as e:
        conn.rollback()
        print(name+"--数据查重失败，有错误，已回滚")


def getContent(mainUrl,pageNum):

    header = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Host': "www.qiushibaike.com",
    'If-None-Match': "cb12690798e4d11fb3055b81b645a2483956124c",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-Site': "none",
    'Sec-Fetch-User': "?1",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }



    allData = r.get(mainUrl,headers=header)

    pageContent = bs(allData.content,"lxml").find("div",{"id":"content-left"}).find_all("div",{"class":"author clearfix"})

    if(len(pageContent)>0):
        print("====第"+str(pageNum)+"页爬取完成,准备解析写入====")

    for item in pageContent:
        name = item.find('img')['alt']
        headimg = "https:"+item.find('img')['src'].split("?")[0]

        insertData(name,headimg)
        time.sleep(1)

    print("====第"+str(pageNum)+"页爬取写入完成====")
    time.sleep(3)


# 24小时  13页  https://www.qiushibaike.com/hot/page/5/
# 热图    13页  https://www.qiushibaike.com/imgrank/page/5/
# 文字    13页  https://www.qiushibaike.com/text/page/13/
# 糗图    35页  https://www.qiushibaike.com/pic/page/5/
# 新鲜    35页  https://www.qiushibaike.com/textnew/page/35
# 以上连接模式雷同，自行替换即可
for pageNum in range(1,endPage):
    if pageNum==1:
        mainUrl= "https://www.qiushibaike.com/hot"
    else:
        mainUrl= "https://www.qiushibaike.com/hot/page/"+str(pageNum)+"/"

    getContent(mainUrl,pageNum)



