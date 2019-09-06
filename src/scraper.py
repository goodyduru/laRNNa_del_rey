import requests
import time
from bs4 import BeautifulSoup
import re
import sys


def get_lyrics(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    raw = soup.find("div", class_="lyrictxt").get_text()
    clean = re.sub(".*\\[.*\n?", "", raw)
    return clean.strip() + "\n\n"


def get_links(site, artist):
    url = site + artist
    response = requests.get(url)

    # get links
    soup = BeautifulSoup(response.text, "html.parser")
    raw = soup.find_all("a", class_="lf-link--primary")
    links = [site + r['href'] for r in raw if artist in str(r)]
    return links


if __name__=="__main__":
    try:
        site = "https://www.lyricsfreak.com"

        raw = input("Please input an artist name: ").strip().lower()
        artist = "/" + raw[0] + "/" + "+".join(raw.split(' ')) + "/"
        links = get_links(site, artist)

        N = len(links)
        n = 1

        scrape = input("There are %d lyrics listed for %s. Continue? Y/N\n" % (N, raw.capitalize()))

        if scrape == "N":
            print("Exiting...")
            sys.exit(0)

        # write to file
        with open("../data/%s_lyrics.txt" % raw, "w+") as f:
            for link in links:
                song_lyrics = get_lyrics(link)
                print("Writing song %d/%d" % (n, N))
                f.write(song_lyrics)
                n += 1

                if n % 20 == 0:
                    time.sleep(20)

            f.close()
    except Exception as e:
        print("Connection refused")
        print(e)


