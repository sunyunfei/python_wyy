#-*- coding: UTF-8 -*-
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#图片保存请求类
class BeautifulUtil():
    #构造方法
    def __init__(self,url,path):
        self.web_url = url
        self.path = path

    #是否需要创建文件
    def mkdir(self):
        path = self.path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print("文件不存在，需要创建")
            os.mkdir(path)
            return True
        else:
            print("文件本地已存在")
            return False

    #请求网络
    def request(self,url):
        r = requests.get(url)
        return r

    #获取文件夹里面的所有文件名称
    def get_files(self):
        files = os.listdir(self.path)
        return files

    #保存图片
    def save_img(self,url,name):
        print("开始请求数据....")
        img = self.request(url)
        print("开始保存图片")
        f = open(name,'ab')
        f.write(img.content)
        print("图片保存成功")
        time.sleep(0.2)
        f.close()

    #处理网络url
    def deal_url(self,str):
        end_pos = str.index('?')
        str = str[:end_pos]
        return str


    #保存全部图片
    def spider(self):
        driver = webdriver.PhantomJS('/Users/syf/Store/python/phantomjs-2.1.1-macosx/bin/phantomjs')
        driver.get(self.web_url)
        #获取到数据所在的iframe
        driver.switch_to.frame('g_iframe')
        html = driver.page_source

        self.mkdir()
        #切换文件里面去，准备生成图片
        os.chdir(self.path)
        #获取文件夹下所有的文件
        file_names = self.get_files()


        #获取到所有的图片
        all_li = BeautifulSoup(html,'lxml').find(id='m-song-module').find_all('li')
        for li in all_li:
            #获取需要的信息
            album_img = self.deal_url(li.find('img')['src'])
            album_name = li.find('p',class_='dec')['title']
            album_date = li.find('span',class_='s-fc3').text
            #进行一次判断名字，如果过长，裁剪
            if len(album_name) >= 50:
                album_name = album_name[:50]
            photo_name = album_date + ' - ' + album_name.replace('/','').replace(':','') +'.jpg'
            print(album_img,photo_name)

            if photo_name in file_names:
                print("已经存在图片，无需下载")
            else:
                self.save_img(album_img,photo_name)



#运行
if __name__ == '__main__':
    b = BeautifulUtil('http://music.163.com/#/artist/album?id=11127&limit=120','/Users/syf/Desktop/photo_img')
    b.spider()