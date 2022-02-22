from consts import *
from hades_wiki_parser import *
from reddit_base import *
from wiki_matcher.wiki import *
from wiki_matcher.match import WikiMatcher
from wiki_matcher.compare import StrCloseComparer

#####################################
class HadesReplyBuilder(ReplyBuilder):
    def __init__(self, wiki):
        self.wiki = wiki
    def build(self, details):
        matches = []
        for k in range(len(details.data)):
            matches.append(details.data[k].full_descr())
        matches.append('[Source Code](https://github.com/TrippW/HadesBot)')
        matches.append(' ^'.join('^This is a bot response'.split(' ')))
        return '\n---\n'.join(matches).replace('\n', '\n\n')

######################################
def make_pages():
    pages = []
    boon_page = WikiPage(f'{wiki_url}/wiki/Boons', BoonParser(BoonIgnorer))
    keepsakes_page = WikiPage(f'{wiki_url}/wiki/Keepsakes', KeepsakeParser(KeepsakeIgnorer))
    legendary_boon_page = WikiPage(f'{wiki_url}/wiki/Legendary_Boons', LegendaryBoonParser(LegendaryIgnorer))
    duo_boon_page = WikiPage(f'{wiki_url}/wiki/Duo_Boons', DuoBoonParser(DuoBoonIgnorer))
    character_page = WikiPage(f'{wiki_url}/wiki/Characters', CharacterParser(CharacterIgnorer))
    companion_page = WikiPage(f'{wiki_url}/wiki/Companions', CompanionParser(CompanionIgnorer))
    mirror_page = WikiPage(f'{wiki_url}/wiki/Mirror_of_Night', MirrorOfNightParser(MirrorOfNightIgnorer))

    pages.append(boon_page)
    pages.append(keepsakes_page)
    pages.append(legendary_boon_page)
    pages.append(duo_boon_page)
    # Not included due to potential noise and lack of actual help
    #pages.append(character_page)
    pages.append(companion_page)
    pages.append(mirror_page)
    
    return pages
    
def run(test=False):
    bot = RedditBot(reddit_scanner_name)
    bot.login()
    bot.connect_subreddit('HadesTheGame')
    wiki_collection = Wiki()
    for page in make_pages():
        wiki_collection.add_page(page)
    wiki_collection.update()
    matcher = WikiMatcher(StrCloseComparer(), BaseIgnorer, wiki_collection, 0.9)
    reply_builder = HadesReplyBuilder(wiki_collection)
    HandlerClass = None
    if test:
        HandlerClass = TestPostHandler
    else:
        HandlerClass = PostHandler
    bot.scan_forever(HandlerClass(matcher, reply_builder).process)

if __name__=='__main__':
    log('Starting program')
    run()
