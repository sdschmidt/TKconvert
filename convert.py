#!/usr/bin/python
# -*- coding: utf-8 -*-
# Convert Tae Kim's guide to japanese 
#
# compiling with errors on pLaTex->dvipdfm
#
# initial version 0.0
# by SDS
import requests
import re
from lxml import html, etree

# base uri
base = 'http://www.guidetojapanese.org'
# where to start
link = '/learn/complete/'

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
    text = ''
    tree = html.fromstring(page.content)
    heading = tree.xpath('//h1/text()')
    text += '\\section{'+heading[0]+'}'
    #print tree.xpath('//h2/text()')
    elist = tree.xpath('//div[contains(@class, "content")]/child::*')
    for element in elist :
        text += getDecendents(element)
        # for each child check if text otherwise get grandchildren
    return text

def getChildren(node) : 
    if type(node) is html.HtmlElement :
        children = node.xpath('child::node()')
        return children
    return 0

def getDecendents(node):
    text = ''
    if type(node) is html.HtmlElement :
        text += getTagStart(node.tag)
        children = getChildren(node)
        for child in children :
            text += getDecendents(child)
        text += getTagEnd(node.tag)
    else :
        text += node.replace('\n', '') # has to be a text node
    return text

def isFollowUp(node):
    return True

def getTagStart(tag):
    if tag is 'p' :
        tagStart = "\n"
    elif tag is 'div' :
        tagStart = ''
    elif tag == "br" :
        tagStart = '\n\n'
    elif tag == "h3" :
        tagStart = '\n\\subsubsection{'
    elif tag == "h2" :
        tagStart = '\n\\subsection{'
    elif tag == "em":
        tagStart = ''
    elif tag == "ul":
        tagStart = '\n\\begin{itemize}\n'
    elif tag == "ol":
        tagStart = '\n\\begin{enumerate}\n'
    elif tag == "li":
        tagStart = '\n\\item '
    else :
        tagStart = ""
    return tagStart

def getTagEnd(tag):
    if tag is 'p' :
        tagEnd = '\\\\'
    elif tag == 'br':
        tagEnd = ''
    elif tag == "h3" :
        tagEnd = '}\n'
    elif tag == "h2" :
        tagEnd = '}\n'
    elif tag == "em":
        tagEnd = ''
    elif tag == "ul":
        tagEnd = '\n\\end{itemize}\n'
    elif tag == "ol":
        tagEnd = '\n\\end{enumerate}\n'
    elif tag == "li":
        tagEnd = ""
    else :
        tagEnd = ""
    return tagEnd

def getTagText(tag) :
    return 0

uri = base+link

i = 0

text =  '\\documentclass[a4paper]{article}\n\n'
text += '\\usepackage{CJKutf8}\n\n'
text += '\\begin{document}\n\n'
text += '\\begin{CJK}{UTF8}{min}\n\n'
while link != 0 and i is not 10 :
    i+=1
    uri = base+link
    page = getPage(uri)
    text += parsePage(page)
    link = getNext(page)
    print i
    print uri

text += '\n\n\end{CJK}\n\n\\end{document}'
text = text.encode('utf8')
text = text.replace('$','\$')
text = text.replace('#','\#')
text = text.replace('‹','LEFT')
text = text.replace('›','RIGHT')
text = text.replace('_','\_')
text = text.replace('&','\&')
with open('main.tex', 'w') as file : 
    file.write(text)
print 'file written'
