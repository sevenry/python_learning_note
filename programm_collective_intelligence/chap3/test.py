
####54页调用generatefeedvector生成blogdata文件失败。是因为feedlist里面的网址无法打开吗？
###downloadzebodata生成zebo.txt也失败。sigh
import clusters

blognames,words,data = clusters.readfile('blogdatadown.txt')#1
#clust = clusters.hcluster(data)
#print (clust)#果然函数中这个值输出也都不一样呢。
#print(blognames)

#clusters.printclust(clust, labels = blognames)#2

#clusters.drawdendrogram(clust, blognames, jpeg = 'blogclust.jpg')#3

rdata = clusters.rotatematrix(data)#4
wordclust = clusters.hcluster(rdata)
clusters.drawdendrogram(wordclust, labels = words, jpeg = 'wordclust.jpg')
'''
kclust = clusters.kcluster(data, k = 4)#5
print ([blognames[r] for r in kclust[0]])
print ([blognames[r] for r in kclust[1]])

import urllib.request#6
from bs4 import BeautifulSoup
c = urllib.request.urlopen('https://en.wikipedia.org/wiki/Jon_Snow')
soup =  BeautifulSoup(c.read(),"lxml")#这里非常有趣！ 感觉有空需要看下这个源代码库呀。
links = soup('a')#所以我还是不懂beautiful soup 的用法呀。
print(links[10])
print(links[10]['href'])
#这一段是教BS的。

wants, people, data = clusters.readfile('zebodown.txt')#7
clust = clusters.hcluster(data, distance = clusters.tanimoto)
clusters.drawdendrogram(clust, wants)

blognames, words, data = clusters.readfile('blogdatadown.txt')
coords = clusters.scaledown(data)
clusters.draw2d(coords, blognames, jpeg = 'blogs2d.jpe')
'''