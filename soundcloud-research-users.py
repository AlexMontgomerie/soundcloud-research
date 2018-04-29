#import libraries: json, re, url
import re
import json
import urllib
from selenium.webdriver import Firefox 
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import time


SCROLL_PAUSE_TIME = 1 

SCROLL = 1 

def getSearchResults(searchUrl):
  #open webpage
  opts = Options()
  opts.set_headless()
  assert opts.headless
  browser = Firefox(options=opts)
  #browser = Firefox()
  browser.get(searchUrl)

  if SCROLL:
    last_height = browser.execute_script("return document.body.scrollHeight")
    scroll_index = 0
    last_height = browser.execute_script("return document.body.scrollHeight")
    timeout = 0
    timeout_max = 1000
    while True:
      timeout+=1
      browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      new_height = browser.execute_script("return document.body.scrollHeight")
      if timeout>=timeout_max:
        break
      if new_height != last_height:
        timeout = 0
        scroll_index += 1
        print("Scroll Index: "+str(scroll_index))
        last_height = new_height

  html = browser.page_source
  browser.quit()
  
  with open('./data/user-page.html', 'w') as outfile:
    outfile.write(html) 
    

#open up html files
# TODO: use beautiful soup instead
def getUsers(filename): 

  f = open(filename,"r")

  userList = []

  #load first line
  line = f.readline()
  user_cnt = 0  
  while line:
    #reset user template
    #parse to find account username
    line = f.readline()
    if re.match("  <h2 class=\"userItem__title\">", line):
      user_cnt += 1
      print('New user found!, user count: '+str(user_cnt))
      #new user matched
      line = f.readline()
      #find username (after previous regex, form of href="/[str]" )
    
      match_tmp = re.match("(\ \ \ \ <a href=\"\/)([a-z,A-Z,0-9,\-]*)",line) #TODO: find 
      userList.append(match_tmp.group(2)) 
  return userList

def getUsers2(filename):
  f = open(filename,'r')
  userDict = {}
  soup = BeautifulSoup(f,"lxml")
  for item in soup.find_all('li'):
    if item.h2:
      user = item.h2.a['href'].replace('/','')
      print('new user, '+user)
      userDict[user] = {}
  return userDict

def saveUserList(filename,userDict):
  data = open(filename).read()
  existingUserDict = json.load(open(filename))
  userDict.update(existingUserDict)
  json.dumps(userDict)
  with open(filename, 'w') as outfile:
    json.dump(userDict, outfile, indent=4) 

def getFollowers(userDict):
  globalUserList = []
  for key in userDict:
    userList = []
    r = requests.get("https://soundcloud.com/"+key+"/followers")
    soup = BeautifulSoup(r.text, "lxml") 
    for item in soup.find_all("a",itemprop="url"):
      user = item['href'].replace('/','')
      if user != key:
        print('new user, '+user)
        userList.append(user)
  
    userDict[key]['followers'] = userList
    globalUserList.extend(userList)

  returnDict = {}
  for user in globalUserList:
    returnDict[user]={}
  return returnDict
  #return [{user} for user in userList]

def getFollowing(userDict):
  userList = []
  r = requests.get("https://soundcloud.com/"+userDict['user']+"/following")
  soup = BeautifulSoup(r.text, "lxml") 
  for item in soup.find_all("a",itemprop="url"):
    user = item['href'].replace('/','')
    print('new user, '+user)
    userList.append(user)
  
  userDict['following'] = userList
  
  return [{'user':user} for user in userList]

searchList =[ 'https://soundcloud.com/search/people?q=islington',
              'https://soundcloud.com/search/people?q=hackney',
              'https://soundcloud.com/search/people?q=hip%20hop&filter.place=london'
            ]

if __name__=="__main__":
  #getFollowers('alexmontgomerie')
  #getFollowing('alexmontgomerie')
  #cleanUserList('./data/users.json')
  #search query
  searchUrl = "https://soundcloud.com/search/people?q=islington"
  #get search results
  #getSearchResults(searchUrl)
  #find users
  #userDict = getUsers2('./data/user-page.html')
  #save to a file
  userDict = {"benzo-enzo": {}}
  userDict.update(getFollowers(userDict))
  saveUserList('./data/users.json',userDict)
  
  ''' 
  for user in userList:
    saveUserList('./data/users.json',getFollowers(user))
    saveUserList('./data/users.json',getFollowing(user))
  '''
