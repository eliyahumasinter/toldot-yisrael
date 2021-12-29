from bs4 import BeautifulSoup
from urllib.request import urlopen
link = "https://www.youtube.com/watch?v=yqL2euapNGE&list=PL8PsmAjtLl4xdvCnPOIZvkMMb0GZgqzzJ"
source = urlopen(link).read()
soup = BeautifulSoup(source, 'lxml')
res=soup.find_all('link')
for i in res:
    print(i)


