#import libraries: json, re, url
import re
import json
import urllib
from selenium.webdriver import Firefox 
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urlparse

class SoundCloud:
  def __init__(self,filename,BROWSER=False):
    self.userDict = {}
    self.SCROLL = 1
    self.currPage = ""
    self.dataFilename = filename
    self.regexGenres =  [
                          [re.compile(r"([H,h]ip[\ -][H,h]op)"),'hip hop'],
                          [re.compile(r"([R,r]ap)"),'rap'],
                          [re.compile(r"([J,j]azz)"),'jazz'],
                          [re.compile(r"([R,r]ock)"),'rock'],
                          [re.compile(r"([H,h]ouse)"),'house'],
                          [re.compile(r"([E,e]lectronic)"),'electronic'],
                          [re.compile(r"([G,r]ime)"),'grime']
                        ]

    self.regexSkills =  [
                          [re.compile(r"([P,p]roducer)"),'producer'],
                          [re.compile(r"([R,r]apper)"),'rapper'],
                          [re.compile(r"([S,s]ing)"),'singer'],
                          [re.compile(r"([G,g]uitar)"),'guitarist'],
                          [re.compile(r"([D,d][J,j])"),'dj'] 
                        ]
    #open webpage
    if BROWSER:
      opts = Options()
      opts.set_headless()
      assert opts.headless
      self.browser = Firefox(options=opts)


  def getSearchResults(self,searchUrl):
    #open webpage
    self.browser.get(searchUrl)

    if self.SCROLL:
      last_height = self.browser.execute_script("return document.body.scrollHeight")
      scroll_index = 0
      timeout = 0
      timeout_max = 1000
      while True:
        timeout+=1
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = self.browser.execute_script("return document.body.scrollHeight")
        if timeout>=timeout_max:
          break
        if new_height != last_height:
          timeout = 0
          scroll_index += 1
          print("Scroll Index: "+str(scroll_index))
          last_height = new_height

    html = self.browser.page_source
    self.currPage = html    
    
  def getUsers(self,filename=0):
    if filename:
      f = open(filename,'r')
      soup = BeautifulSoup(f,"lxml")
    else:
      soup = BeautifulSoup(self.currPage,"lxml")
    for item in soup.find_all('li'):
      if item.h2:
        user = item.h2.a['href'].replace('/','')
        print('new user, '+user)
        self.userDict[user] = {}

  def updateUserDict(self):
    existingUserDict = json.load(open(self.dataFilename))
    existingUserDict.update(self.userDict)
    self.userDict
    tmpDict = self.userDict
    json.dumps(tmpDict)
    with open(self.dataFilename, 'w') as outfile:
      json.dump(tmpDict, outfile, indent=4) 

  def saveUserDict(self):
    tmpDict = self.userDict
    json.dumps(tmpDict)
    with open(self.dataFilename, 'w') as outfile:
      json.dump(tmpDict, outfile, indent=4) 

  def loadUserDict(self):
    self.userDict = json.load(open(self.dataFilename))

  def getFollowers(self,update=True,forceUpdate=False):
    globalUserList = []
    for key in self.userDict:
      if self.userDict[key]!={} and not forceUpdate:
        continue
      userList = []
      r = requests.get("https://soundcloud.com/"+key+"/followers")
      soup = BeautifulSoup(r.text, "lxml") 
      for item in soup.find_all("a",itemprop="url"):
        user = item['href'].replace('/','')
        if user != key:
          print('new user, '+user)
          userList.append(user)
  
      self.userDict[key]['followers'] = userList
      globalUserList.extend(userList)

    if update:
      for user in globalUserList:
        if user not in self.userDict:
          self.userDict[user] = {}

  def getFollowing(self,update=True,forceUpdate=False):
    globalUserList = []
    for key in self.userDict:
      if self.userDict[key]!={} and not forceUpdate:
        continue
      userList = []
      r = requests.get("https://soundcloud.com/"+key+"/following")
      soup = BeautifulSoup(r.text, "lxml") 
      for item in soup.find_all("a",itemprop="url"):
        user = item['href'].replace('/','')
        if user != key:  
          print('new user, '+user)
          userList.append(user)
  
      self.userDict[key]['following'] = userList
      globalUserList.extend(userList)
 
    if update:
      for user in globalUserList:
        if user not in self.userDict:
          self.userDict[user] = {}

  def getUserInfo(self,forceUpdate=False):
  
    #go through all users
    for user in self.userDict:
      if self.userDict[user]!={} and not forceUpdate:
        continue
      print('processing user: '+user)
      response = requests.get('https://soundcloud.com/'+user)
      html = response.text
      html = html.split('\n')
      for line in html:
        match_tmp = re.match("(\ \ <script>webpackJsonp\(\[\],)(.*?)(\);<\/script>)",line)
        if match_tmp:
          json_data = match_tmp.group(2)

          followings_count      = re.search('(followings_count\":)([0-9]+(,[0-9]+)*)',json_data)
          followers_count       = re.search('(followers_count\":)([0-9]+(,[0-9]+)*)',json_data)
          track_count           = re.search('(track_count\":)([0-9]+(,[0-9]+)*)',json_data)
          reposts_count         = re.search('(reposts_count\":)([0-9]+(,[0-9]+)*)',json_data)
          playlist_count        = re.search('(playlist_count\":)([0-9]+(,[0-9]+)*)',json_data)
          comments_count        = re.search('(comments_count\":)([0-9]+(,[0-9]+)*)',json_data)
          city                  = re.findall('(city\":\")(.*?)(\")',json_data)
          description           = re.search('(description\":\")(.*?)(\")',json_data)
          likes_count           = re.search('(\"likes_count\":)([0-9]+(,[0-9]+)*)',json_data)
          playlist_likes_count  = re.search('(\"playlist_likes_count\":)([0-9]+(,[0-9]+)*)',json_data)
          username              = re.search('(username\":\")(.*?)(\")',json_data)
          country_code          = re.findall('(country_code\":\")(.*?)(\")',json_data)

          if country_code:
            if len(country_code)==2:
              self.userDict[user]["country_code"] = country_code[1][1]

          if followings_count:
            self.userDict[user]["followings_count"] = followings_count.group(2)

          if followers_count:
            self.userDict[user]["followers_count"] = followers_count.group(2)

          if track_count:
            self.userDict[user]["track_count"] = track_count.group(2)
          
          if reposts_count:
            self.userDict[user]["reposts_count"] = reposts_count.group(2)
  
          if playlist_count:
            self.userDict[user]["playlist_count"] = playlist_count.group(2)

          if comments_count:
            self.userDict[user]["comments_count"] = comments_count.group(2)

          if city:
            if len(city)==2:
              self.userDict[user]["city"] = city[1][1]

          if description:
            self.userDict[user]["description"] = description.group(2)
            
            self.userDict[user]["skills"] = []
            self.userDict[user]["genres"] = []
            
            for regex in self.regexSkills:
              skill_tmp = regex[0].search(self.userDict[user]["description"])
              if skill_tmp:
                self.userDict[user]["skills"].append(regex[1])
 
            for regex in self.regexGenres:
              genre_tmp = regex[0].search(self.userDict[user]["description"])
              if genre_tmp:
                self.userDict[user]["genres"].append(regex[1])
 
          if likes_count:
            self.userDict[user]["likes_count"] = likes_count.group(2)

          if playlist_likes_count:
            self.userDict[user]["playlist_likes_count"] = playlist_likes_count.group(2)

          if username:
            self.userDict[user]["username"] = username.group(2) 
 
          #parse description
       
          break

  #TODO: clean up returned links 
  def getUserInfoLinks(self,forceUpdate=False):
    for user in self.userDict:
      if self.userDict[user]!={} and not forceUpdate:
        continue
      print('processing user (links): '+user)
      self.browser.get("https://soundcloud.com/"+user)
      response = self.browser.page_source
      soup = BeautifulSoup(response, "lxml")
      self.userDict[user]['links'] = []
      for item in soup.find_all("li", class_="web-profiles__item"):
        res = urlparse(item.div.a['href'])
        if res.scheme=='mailto':
          self.userDict[user]['links'].append(res.path)
        if res.scheme=='https':
          self.userDict[user]['links'].append(res.query) 


  def filterCountryCode(self,countryCode='GB'):
    rm_count = 0
    rmList = []
    for user in self.userDict:
      if 'country_code' in self.userDict[user]:
        if self.userDict[user]['country_code'] != countryCode:
         rmList.append(user)
    
    for user in rmList:
      rm_count+=1
      print('removing '+user)
      del self.userDict[user] 
    print('Number Removed: '+str(rm_count))

  def getUserDictSize(self):
    return len(self.userDict)

  def saveUserList(self,filename):
    userList = []
    for user in self.userDict:
      userList.append(user)
    json.dumps(userList)
    with open(filename, 'w') as outfile:
      json.dump(userList, outfile, indent=4) 

  def scrollPage(self):
    last_height = self.browser.execute_script("return document.body.scrollHeight")
    scroll_index = 0
    timeout = 0
    timeout_max = 1000
    while True:
      timeout+=1
      self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      new_height = self.browser.execute_script("return document.body.scrollHeight")
      if timeout>=timeout_max:
        break
      if new_height != last_height:
        timeout = 0
        scroll_index += 1
        print("Scroll Index: "+str(scroll_index))
        last_height = new_height

  def getFollowersAll(self,update=True,forceUpdate=False):
    globalUserList = []
    for key in self.userDict:
      if self.userDict[key]!={} and not forceUpdate:
        continue
      userList = []
      self.browser.get('https://soundcloud.com/'+key+'/followers')
      self.scrollPage()
      html = self.browser.page_source
      soup = BeautifulSoup(html, "lxml") 
      for item in soup.find_all("a",itemprop="url"):
        user = item['href'].replace('/','')
        if user != key:
          print('new user, '+user)
          userList.append(user)
  
      self.userDict[key]['followers'] = userList
      globalUserList.extend(userList)

    if update:
      for user in globalUserList:
        if user not in self.userDict:
          self.userDict[user] = {}

  def getFollowingAll(self,update=True,forceUpdate=False):
    globalUserList = []
    for key in self.userDict:
      if self.userDict[key]!={} and not forceUpdate:
        continue
      userList = []
      self.browser.get('https://soundcloud.com/'+key+'/following')
      self.scrollPage()
      html = self.browser.page_source
      soup = BeautifulSoup(html, "lxml") 
      for item in soup.find_all("a",itemprop="url"):
        user = item['href'].replace('/','')
        if user != key:  
          print('new user, '+user)
          userList.append(user)
  
      self.userDict[key]['following'] = userList
      globalUserList.extend(userList)
 
    if update:
      for user in globalUserList:
        if user not in self.userDict:
          self.userDict[user] = {}

   

searchList =[ 'https://soundcloud.com/search/people?q=islington',
              'https://soundcloud.com/search/people?q=hackney',
              'https://soundcloud.com/search/people?q=hip%20hop&filter.place=london'
            ]

if __name__=="__main__":
  searchUrl = "https://soundcloud.com/search/people?q=islington"
  sc = SoundCloud('./data/users.json')
  #sc.getSearchResults(searchUrl)
  sc.loadUserDict()
  #sc.getUsers() 
  #sc.getUserInfo() 
  #sc.getUserInfoLinks()
  sc.getFollowers()
  sc.getUserInfo() 
  sc.filterCountryCode()
  print(sc.getUserDictSize())
  sc.updateUserDict()
