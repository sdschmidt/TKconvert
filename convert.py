import requests
import re
from lxml import html, etree
from io import StringIO, BytesIO

base = 'http://www.guidetojapanese.org'

def getPage(uri) :
    page = requests.get(uri)
    return page

def getNext(page) :
    tree = html.fromstring(page.content)
    link = tree.xpath('//a[@class="page-next"]/@href')
    if len(link) != 0 :
        return link[0]
    return 0

def parsePage(page) : # html -> latex
    tree = html.fromstring(page.content)
    #print tree.xpath('//h1/text()')
    #print tree.xpath('//h2/text()')
    elist = tree.xpath('//div[contains(@class, "content")]/child::*')
    
    for element in elist :
        getDecendents(element)
        # for each child check if text otherwise get grandchildren
    return 0

def getChildren(node) : 
    if type(node) is html.HtmlElement :
        children = node.xpath('child::node()')
        return children
    return 0

def getDecendents(node):
    if type(node) is html.HtmlElement :
        print "START "+node.tag
        children = getChildren(node)
        for child in children :
            getDecendents(child)
        print "END "+node.tag
    else :
        print node # has to be a text node
    return 0


class EchoTarget(object) :
    def start(self, tag, attrib):
        print("start %s %r" % (tag, dict(attrib)))
    def end(self, tag):
        print("end %s" % tag)
    def data(self, data):
        print("data %r" % data)
    def comment(self, text):
        print("comment %s" % text)
    def close(self):
        print("close")
        return "closed!"


link = '/learn/complete/stateofbeing'
uri = base+link

i = 0
#while link != 0 :
i+=1
uri = base+link
print uri
page = getPage(uri)
parsePage(page)
link = getNext(page)

print i
