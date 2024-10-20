import sys
import time
import requests
from bs4 import BeautifulSoup

url = sys.argv[1]
video_ext = ('.mkv', '.avi', '.mp4')

html_page = requests.get(url).text
soup = BeautifulSoup(html_page, "lxml")
a = soup.find_all('a')

# x = soup.find('div', attrs={'id':"notification"})
# print(x)

with open(f'{int(time.time())}.m3u', 'w') as f:
    for i in a:
        if i.get('href').endswith(video_ext):
            f.write(url.split('/FTP-5')[0] + i.get('href') + '\n')