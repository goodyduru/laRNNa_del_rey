import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re


def get_lyrics(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    raw = soup.find("div", class_="lyrictxt").get_text()
    clean = re.sub(".*\\[.*\n?", "", raw)
    return clean.strip()


def get_links(site, artist):
    url = site + artist
    response = requests.get(url)

    # get links
    soup = BeautifulSoup(response.text, "html.parser")
    raw = soup.find_all("a", class_="lf-link--primary")
    links = [site + r['href'] for r in raw if artist in str(r)]
    return links


if __name__=="__main__":
    site = "https://www.lyricsfreak.com"
    artist = "/l/lana+del+rey/"
    links = get_links(site, artist)

    N = len(links)
    n = 1

    # write to file
    with open("../out/lana_lyrics.txt", "w+") as f:
        for link in links:
            song_lyrics = get_lyrics(link)
            print("Writing song %d/%d" % (n, N))
            f.write(song_lyrics)
            n += 1

            if n % 20 == 0:
                time.sleep(60)

        f.close()

