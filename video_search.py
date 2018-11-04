from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

textToSearch = 'bananas'
query_string = urllib.parse.urlencode({"search_query" : textToSearch})
html = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
soup = BeautifulSoup(html, features="html.parser")
vid = soup.find(attrs={'class':'yt-uix-tile-link'})
print('https://www.youtube.com' + vid['href'])
