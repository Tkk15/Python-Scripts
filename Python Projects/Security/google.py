'''
Put the file in same folder as the one from where you are running python.

Dependencies:
requests	(apt-get install python-requests, or pip install python-requests)
bs4		(apt-get install python-bs4, or pip install python-bs4)
Have them installed before runningthe script.

Usage is simple:
1.For text search:

import google
s=gogole.searcher()
results=s.textsearch(string_to_be_searched)
print results['head']
print results['url']
print results['description']

2.For translator

import google
t=google.translator()
translated_string=t.translate(string_to_be_translated,target_language_name)

//Source language is detected automatically,by default target language is hindi
//You can view languages available by t.listlangs()

'''
#Mon Aug 18 12:31:40 IST 2014

import sys
import re
import requests
import json
from bs4 import BeautifulSoup
  
class translator():
  def __init__(self):
    self.url='https://translate.google.com/translate_a/single'
    self.user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/29.0.1547.65 Chrome/29.0.1547.65 Safari/537.36'}
    self.default_tlang="Hindi"
    self.timeout=20
    self.arg_re=re.compile(r"(@\w+=)(\w+)")
    self.punct_re=re.compile(r'[./<>;\':\"\[\]{}\\~@#$%^&*()-=`|]')
    self.ex_re=re.compile(r'[\[\]\'"\\/]')
    self.langdict={
		    'Afrikaans':'af',
		    'Albanian':'sq',
		    'Arabic':'ar',
		    'Armenian':'hy',
		    'Azerbaijani':'az',
		    'Basque':'eu',
		    'Belarusian':'be',
		    'Bengali':'bn',
		    'Bosnian':'bs',
		    'Bulgarian':'bg',
		    'Catalan':'ca',
		    'Cebuano':'ceb',
		    'Chinese':'zh-CN',
		    'Croatian':'hr',
		    'Czech':'cs',
		    'Danish':'da',
		    'Dutch':'nl',
		    'English':'en',
		    'Esperanto':'eo',
		    'Estonian':'et',
		    'Filipino':'tl',
		    'Finnish':'fi',
		    'French':'fr',
		    'Galician':'gl',
		    'Georgian':'ka',
		    'German':'de',
		    'Greek':'el',
		    'Gujarati':'gu',
		    'Haitian Creole':'ht',
		    'Hausa':'ha',
		    'Hebrew':'iw',
		    'Hindi':'hi',
		    'Hmong':'hmn',
		    'Hungarian':'hu',
		    'Icelandic':'is',
		    'Igbo':'ig',
		    'Indonesian':'id',
		    'Irish':'ga',
		    'Italian':'it',
		    'Japanese':'ja',
		    'Javanese':'jw',
		    'Kannada':'kn',
		    'Khmer':'km',
		    'Korean':'ko',
		    'Lao':'lo',
		    'Latin':'la',
		    'Latvian':'lv',
		    'Lithuanian':'lt',
		    'Macedonian':'mk',
		    'Malay':'ms',
		    'Maltese':'mt',
		    'Maori':'mi',
		    'Marathi':'mr',
		    'Mongolian':'mn',
		    'Nepali':'ne',
		    'Norwegian':'no',
		    'Persian':'fa',
		    'Polish':'pl',
		    'Portuguese':'pt',
		    'Punjabi':'pa',
		    'Romanian':'ro',
		    'Russian':'ru',
		    'Serbian':'sr',
		    'Slovak':'sk',
		    'Slovenian':'sl',
		    'Somali':'so',
		    'Spanish':'es',
		    'Swahili':'sw',
		    'Swedish':'sv',
		    'Tamil':'ta',
		    'Telugu':'te',
		    'Thai':'th',
		    'Turkish':'tr',
		    'Ukrainian':'uk',
		    'Urdu':'ur',
		    'Vietnamese':'vi',
		    'Welsh':'cy',
		    'Yiddish':'yi',
		    'Yoruba':'yo',
		    'Zulu':'zu'
		  }
    self.google_url='https://translate.google.com/translate_a/single'
    
  def translate(self,query,tlang='hindi'):
    query=self.punct_re.sub(r'',query)
    tlangcode=self.getlangcode(tlang)
    if tlangcode==1:
      return "<Couldnt find language code for "+tlang+">"
    
    payload={
	   'client':'t',
	   'sl':'auto',
	   'tl':tlangcode,
	   'dt':'bd',
	   'dt':'ex',
	   'dt':'ld',
	   'dt':'md',
	   'dt':'qc',
	   'dt':'rw',
	   'dt':'rm',
	   'dt':'ss',
	   'dt':'t',
	   'ie':'UTF-8',
	   'oe':'UTF-8',
	   'prev':'enter',
	   'rom':'1',
	   'ssel':0,
	   'tsel':4,
	   'q':'\''+query+'\''
	   }
    
    try:
      response=requests.get(self.url,headers=self.user_agent,params=payload,timeout=self.timeout)
      text=self.ex_re.sub(r'',(response.text).encode('utf-8'))
      try:
	text=text.split(',')[0]
	return text.strip()
      except:
	return "<Error parsing translated text>"
    except:
      return "Connection Error."
  
  def getlangcode(self,langstring):
    try:
      return self.langdict[(langstring.lower()).title()]
    except:
      return 1 #1 for Error
    
  def listlangs(self):
    for i in sorted(self.langdict.keys()):
      print i

class searcher:
  def __init__(self):
    self.user_agent={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/29.0.1547.65 Chrome/29.0.1547.65 Safari/537.36'}
    self.tag_r=re.compile(r'<.*?.>')

  def textsearch(self,query):
    payload={'q':query}
    response=requests.get("http://www.google.com/search", headers = self.user_agent,params=payload)
    soup=BeautifulSoup(response.text)
    baddata=soup.findAll('li',{'class':'g'})
    heads=[]
    urls=[]
    descrips=[]
    for data in baddata:
      soup=BeautifulSoup(str(data))
      try:
	heads.append(str(soup.findAll("h3",{"class":"r"})[0]))
      except:
	heads.append("")
      try:
	urls.append(str(soup.findAll("cite",{"":""})[0]))
      except:
	urls.append("")
      try:
	descrips.append(str(soup.findAll("span",{"class":"st"})[0]))
      except:
	descrips.append("")
    results={'head':[],'url':[],'description':[]}
    for i in range(0,len(heads)):
      results['head'].append(self.tag_r.sub(r'',heads[i]))
      results['url'].append(self.tag_r.sub(r'',urls[i]))
      results['description'].append(self.tag_r.sub(r'',descrips[i]))
    return results
  def imagesearch(self):
    return("<Not Implemented Yet>")
    
  
      
def main():
  translator_i=translator()
  try:
    text=" ".join(sys.argv[1:])
    if text=='@list':
      translator_i.listlangs()
      return
    query=text.split('@')[0]
    bad_args=(translator_i.arg_re).findall(text)
    if len(bad_args)>1:
      print "<Usage:> query_string @t=target_lang (By default it converts to hindi)>\nPass query_string \"@list\" to get list of languages available."
      return
	  
    for item in bad_args:
	if item[0]=='@t=':
	  tlang=item[1]
	  break
	
  except:
    print "<Error While Processing Query>"
    return
  
  try:
    tlang=tlang
  except:
    tlang=translator_i.default_tlang
  if not tlang:
    tlang=translator_i.default_tlang
  translated_text=translator_i.translate(query, tlang)  
  print translated_text

if (__name__ == '__main__'):
    main()