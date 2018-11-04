import bs4 as bs
import urllib.request

url = "http://www.quotationspage.com/search.php?Search=mad"
page = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(page, features="html.parser")

quoteslist = []
def find_img(soup):
    for img in soup.find_all('dt', {'class':'quote'}):
        imgcon = img.find('a')
        imgsource = imgcon.text
        print(imgsource)
        quoteslist.append(imgsource)

find_img(soup)
print(quoteslist)
