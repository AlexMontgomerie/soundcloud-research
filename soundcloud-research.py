#import libraries: json, re, url
import re
import json
import urllib

#open up html files
def getUsers(filename): 

  f = open(filename,"r")

  userList = []

  #load first line
  line = f.readline()
  while line:
    #reset user template
    #parse to find account username
    line = f.readline()
    if re.match("  <h2 class=\"userItem__title\">", line):
      #new user matched
      line = f.readline()
      #find username (after previous regex, form of href="/[str]" )
    
      match_tmp = re.match("(\ \ \ \ <a href=\"\/)([a-z,A-Z,0-9,\-]*)",line) #TODO: find 
      userList.append(match_tmp.group(2)) 
  return userList

def getUserInfo(userList):
  #go through all users
  for user in userList:
    response = urllib.urlopen('https://soundcloud.com/'+user)
    html = response.read()
    html = html.split('\n')
    #print(html)
    for line in html:
      match_tmp = re.match("(\ \ <script>webpackJsonp\(\[\],)(.*?)(\);<\/script>)",line)
      #print(line)
      if match_tmp:
        json_tmp = match_tmp.group(2)
        print(json_tmp)
        print(json.load(json_tmp))
        break

if __name__=="__main__":
  filename = "./data/soundcloud-hiphop.html"
  userList = getUsers(filename)
  getUserInfo(['robotrump'])

  
