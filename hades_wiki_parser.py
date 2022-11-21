from bs4 import BeautifulSoup

from consts import wiki_url
from hades_wiki_items import *
from wiki_matcher.wiki_parser import PageParser

class BoonParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        for body in soup.findAll('tbody'):
            god_name = ' '.join(body.findParent().find('caption').text.strip().split(' ')[:-1])
            for row in body.findAll('tr'):
                data = row.findChildren('td', recursive=False)
                if data:
                    items.append([god_name, *data])
        return items

    def create_item(self, data):
        return Boon(data[0], data[1].find('p').text.strip(), data[2].text.strip())

class DuoBoonParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        for body in soup.findAll('tbody'):
            god_name = body.findParent().find('caption').text.strip()[:-1]
            for row in body.findAll('tr'):
                data = row.findChildren('td', recursive=False)
                if data:
                    items.append(data)
        return items

    def create_item(self, data):
        return DuoBoon(data[0].text.replace('\n', ''), data[1].text, data[2].text.replace(' ', '').replace('\n', '').split('/'), data[3].text)

class KeepsakeParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        for row in soup.find('span', {'id':'List_of_keepsakes'}).findNext('tbody').findAll('tr'):
            data = row.findChildren('td', recursive=False)
            if data:
                items.append(data)
        return items

    def create_item(self, data):
        return Keepsake(data[0].text.strip(), data[1].text.strip(), data[2].text.strip())

class LegendaryBoonParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        body = soup.find('span', {'id':'Legendary_Boons'}).findNext('tbody')
        rows = body.findAll('tr')
        for row in body.findAll('tr')[1:]:
            data = row.findChildren('td', recursive=False)
            if data:
                items.append(data)
        return items

    def create_item(self, data):
        return LegendaryBoon(data[0].text.replace('\n', ''), data[1].text, data[2].text.replace(' ', '').replace('\n', ''), data[3].text)

class CharacterParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        table = soup.find('table', {'class':'navbox'})
        for data in table.findChildren('a', recursive=True):
            if data and 'title' in data.attrs and 'href' in data.attrs:
                item = [data['title'], f'{wiki_url}{data["href"]}']
                items.append(item)
        return items[2:]

    def create_item(self, data):
        return Character(*data)

class CompanionParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        for row in soup.find('span', {'id':'List_of_Companions'}).findNext('tbody').findAll('tr'):
            data = row.findChildren('td', recursive=False)
            if data:
                items.append(data)
        return items

    def create_item(self, data):
        return Companion(data[0].text.strip(), data[1].text.strip(), data[2].text.strip())


class MirrorOfNightParser(PageParser):
    def find_items(self, soup: BeautifulSoup):
        items = []
        for row in soup.find('span', {'id':'Talents'}).findNext('tbody').findAll('tr'):
            data = row.findChildren('td', recursive=False)
            if data:
                items.append(data[:4])
                items.append(data[4:])
        return items

    def create_item(self, data):
        return MirrorOfNightTalents(data[0].text.replace('\n', ' ').strip(), data[1].text.strip(), data[2].text.replace('\n', ' ').strip())


