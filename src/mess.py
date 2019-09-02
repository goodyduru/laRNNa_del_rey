import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

url = 'https://www.lyricsfreak.com/l/lana+del+rey/13+beaches_21148819.html'
response = requests.get(url)

# get lyrics
soup = BeautifulSoup(response.text, "html.parser")
raw = soup.find("div", class_="lyrictxt").get_text()
clean = re.sub(".*\\[.*\n?", "", raw)
print(clean)