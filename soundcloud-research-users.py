#import libraries: json, re, url
import re
import json
import urllib
from selenium.webdriver import Firefox 
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
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
    '''
    while True:
      scroll_index += 1
      print("Scroll Index: "+str(scroll_index))
      browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(SCROLL_PAUSE_TIME)
      new_height = browser.execute_script("return document.body.scrollHeight")
      timeout = 0
      timeout_max = 100000000000
      while new_height!=last_height:
        timeout+=1
        if timeout==timeout_max:
          print('timeout on scroll')
          break
      if timeout==timeout_max:
        break 
      timeout = 0
      last_height = new_height
    '''
    last_height = browser.execute_script("return document.body.scrollHeight")
    timeout = 0
    timeout_max = 1000000
    while True:
      timeout+=1
      browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      new_height = browser.execute_script("return document.body.scrollHeight")
      if timeout>=timeout_max:
        break
      if new_height != last_height:
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

if __name__=="__main__":
  #search query
  searchUrl = "https://soundcloud.com/search/people?q=hip%20hop&filter.place=london"
  #get search results
  getSearchResults(searchUrl)
  #find users
  userList = getUsers('./data/user-page.html')
  #save to a file
  json.dumps(userList)
  with open('./data/users.json', 'a') as outfile:
    json.dump(userList, outfile, indent=4, sort_keys=True) 

