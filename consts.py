import datetime

from wiki_matcher.ignore import ListIgnorer, Ignorer

wiki_url = 'https://hades.fandom.com'
empty_ignorer = ListIgnorer([])

BaseIgnorer = ListIgnorer(["death defiance", "deaths defiance", "death defiances", "deaths defiances", "death's defiance", "death defiance's", "death's defiance's"])
BoonIgnorer = empty_ignorer
KeepsakeIgnorer = empty_ignorer
LegendaryIgnorer = empty_ignorer
DuoBoonIgnorer = empty_ignorer
CharacterIgnorer = ListIgnorer(['hades', 'other', 'codex', 'heres'])
CompanionIgnorer = empty_ignorer
MirrorOfNightIgnorer = ListIgnorer(["death defiance", "deaths defiance", "death defiances", "deaths defiances", "death's defiance", "death defiance's", "death's defiance's"])

reddit_scanner_name='hades'

def log(text):
    """helper to log to file and print at the same time"""
    with open(reddit_scanner_name+'.log', 'a', encoding='utf-8') as logger:
        log_text = text.replace('\n', '\n\t')
        logger.write(f'\n{str(datetime.datetime.utcnow())}: {log_text}')
    print(text)
