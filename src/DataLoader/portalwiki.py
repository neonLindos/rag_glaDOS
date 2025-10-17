from bs4 import BeautifulSoup
import requests

portal_wiki = "https://theportalwiki.com/wiki/GLaDOS_voice_lines_(Portal_2)"
combineoverwiki = "https://combineoverwiki.net/wiki/GLaDOS/Quotes/Portal_2_single-player"

headers = {
    "Host": "combineoverwiki.net",
    "Cookie": "bpc=ad4124881879071577baf3583b26fc2c",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "If-Modified-Since": "Sat, 13 Sep 2025 05:14:24 GMT",
    "Connection": "keep-alive"
}


class WikiParser:

    def __init__(self):
        # Для PortalWiki
        self.portalwiki_chapters = {}
        self.portalwiki_glados = {}

        # Для CombineOverWiki
        self.combineoverwiki_chapters = {}

    def get_dialogues_portalwiki(self):
        req = requests.get(portal_wiki)
        soup = BeautifulSoup(req.text, 'lxml')

        current_chapter = None

        for tag in soup.find_all(['h3', 'i']):
            if tag.name == 'h3':
                current_chapter = tag.get_text(strip=True)
                self.portalwiki_chapters[current_chapter] = []
            elif tag.name == 'i' and current_chapter:
                line = tag.get_text(strip=True)
                self.portalwiki_chapters[current_chapter].append(line)

        # главы с упоминанием GLaDOS
        for chapter, lines in self.portalwiki_chapters.items():
            if any("GLaDOS" in line or "GlaDOS" in line for line in lines):
                self.portalwiki_glados[chapter] = lines

    def get_dialogues_combineoverwiki(self):
        req = requests.get(url=combineoverwiki,headers=headers)
        print(req.text)

        

    def print_chapters(self):
        print("== PortalWiki: Все главы ==")
        for chapter, lines in self.portalwiki_chapters.items():
            print(f"\n{chapter}")
            for line in lines:
                print(line)

        print("\n== PortalWiki: Главы с GLaDOS ==")
        for chapter, lines in self.portalwiki_glados.items():
            print(f"\n{chapter}")
            for line in lines:
                print(line)

        print("\n== CombineOverWiki: Все главы ==")
        for chapter, lines in self.combineoverwiki_chapters.items():
            print(f"\n{chapter}")
            for time, quote in lines:
                print(f"{time}: {quote}")

    def save_chapters_to_file(self, filename="chapters.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("== PortalWiki: Все главы ==\n")
            for chapter, lines in self.portalwiki_chapters.items():
                f.write(f"\n{chapter}\n")
                for line in lines:
                    f.write(f"{line}\n")

            f.write("\n== PortalWiki: Главы с GLaDOS ==\n")
            for chapter, lines in self.portalwiki_glados.items():
                f.write(f"\n{chapter}\n")
                for line in lines:
                    f.write(f"{line}\n")

            f.write("\n== CombineOverWiki: Все главы ==\n")
            for chapter, lines in self.combineoverwiki_chapters.items():
                f.write(f"\n{chapter}\n")
                for time, quote in lines:
                    f.write(f"{time}: {quote}\n")

        print(f"Все данные сохранены в {filename}")


