#pylint: skip-file 
import requests
import re
import os
from pyquery import PyQuery as jq
from lxml import etree

def processTopicLink(page, topicUrl):
  print('>>>>> 分析话题列表...', topicUrl)
  def filterLink(index, node):
    if (node.attrib['title'].find('晒') > -1):
      arry.append(node.attrib['href'])
    
  arry = []
  doc = jq(page)
  result = doc('td.title a')
  # result.each(lambda index,node: arry.append(node.attrib['href']))
  result.each(filterLink)
  return arry 

def processDetailImageURL(detailPage, topicUrl):
  print('>>>>> 分析话题', topicUrl, '中的图片')
  arry = []
  doc = jq(detailPage)
  result = doc('.topic-figure img')
  result.each(lambda index,node: arry.append(node.attrib['src']))
  return arry 

def processTopicList(url):
  maxPageNo = 10
  pageSize = 25
  pageNo = 0
  topicArray = []
  while (pageNo < maxPageNo):
    topicArray.extend(processTopicLink(getData(url, {'start': pageNo * pageSize}), url + '?pageNo=' + str(pageNo)))
    pageNo+=1
  return topicArray

def getData(url, param={}):
  res = requests.get(url, params=param).content
  # print(res)
  return res

def saveImage(imgList):
  i = 0
  path = './img/'
  if not os.path.exists(path):
    os.makedirs(path)
  
  while i < len(imgList):
    print('>>>>> Geting img: ', imgList[i])
    imgBuffer = requests.get(imgList[i]).content
    fileName = re.findall(r'(\w+.jpg)', imgList[i])[0]
    filePath = path + fileName
    output = open(filePath, 'wb')
    output.write(imgBuffer)
    i+=1

  print('共计',len(imgList),'张图片')

def go():
  imgLink = []
  print('准备中...')
  url = 'https://www.douban.com/group/haixiuzu/discussion'
  topicLink = processTopicList(url)
  for link in topicLink:
    imgLink.extend(processDetailImageURL(getData(link), link))
  saveImage(imgLink)
  print('完毕!')

if __name__ == '__main__':
  go()