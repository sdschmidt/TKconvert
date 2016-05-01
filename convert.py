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
    elist = tree.xpath('//div[contains(@class, "content")]/descendant::*/text()')
    text = ''
    for element in elist :
        tag = element.getparent().tag
        element.replace(
        if tag == 'h2':
            text += '\n\n>> '+element+' << \n\n '
        elif tag == 'h3':
            text += '\n\n>> '+element+'\n\n '
        elif tag == 'p' :
            text += '\n    ' + element
        elif tag == 'li' :
            text += ' ** ' + element
        else :
            text += element
    print text
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
