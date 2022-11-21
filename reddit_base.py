import traceback
import os
import datetime

import praw
import prawcore
from abc import ABC, abstractmethod
from consts import log

def _get_post_created_as_datetime(post):
    return datetime.datetime.fromtimestamp(post.created_utc)

class ReplyBuilder(ABC):
    @abstractmethod
    def build(self, details):
        pass

class PostHandler:
    def __init__(self, matcher, reply_builder):
        self.matcher = matcher
        self.reply_builder = reply_builder
    
    def update(self):
        self.matcher.wiki.update();
    
    def process(self, post):
        matchDetails = self.matcher.match(post)
        if matchDetails.has_match():
            self.do_post(post, self.reply_builder.build(matchDetails))

    def do_post(self, post, reply):
        if isinstance(post, praw.models.Comment) \
        or isinstance(post, praw.models.Submission):
            log(f'url: {post.permalink}')
        log(f'generated reply: \n{reply}')
        post.reply(reply)

class TestPostHandler(PostHandler):
    def do_post(self, post, reply):
        if isinstance(post, praw.models.Comment) \
        or isinstance(post, praw.models.Submission):
            log(f'url: {post.permalink}')
        print('-'*50)
        print('title:', post.title)
        print('body:', post.selftext)
        print('-'*10, 'reply', '-'*10, sep='')
        log(reply)
    
class RedditBot:
    session=None
    subreddit=None
    checked_ids = []
    name=''

    def _checked_filename(self):
        return f'{self.name}_checked.txt'
    
    def __init__(self, name):
        self.name = name
        self.FORCE_WIKI_UPDATE_FILEPATH = f'{name}.update'
        self.load_checked_ids()

    def _write_last_processed_utc_to_file(self, append=True):
        with open(self._checked_filename(), 'a' if append else 'w') as file:
            if append:
                file.write('\n')
            file.write(self.last_processed_utc.isoformat())

    def load_checked_ids(self):
        if not os.path.exists(self._checked_filename()) \
        or os.path.getsize(self._checked_filename()) == 0:
            self.last_processed_utc = datetime.datetime.utcnow()
            log(f'creating id file')
        else:
            with open(self._checked_filename(), 'r') as file:
                s = file.readlines()
                self.last_processed_utc = datetime.datetime.fromisoformat(s[-1])
        self._write_last_processed_utc_to_file(False)
        log(f'set last processed: {self.last_processed_utc.isoformat()}')
                
    def mark_checked(self, post):
        self.last_processed_utc = _get_post_created_as_datetime(post)
        self._write_last_processed_utc_to_file()
    
    def login(self):
        self.session = praw.Reddit(redirect_uri='http://localhost:8080',
                           user_agent=f'{self.name} bot by /u/devTripp')

    def connect_subreddit(self, subreddit_name):
        self.subreddit=self.session.subreddit(subreddit_name)

    def is_new_post(self, post):        
        return ((post is not None)
                and (_get_post_created_as_datetime(post) > self.last_processed_utc))
    
    def scan(self, handler: PostHandler=None):
        for post in self.subreddit.stream.submissions():
            if self.is_new_post(post):
                if os.path.exists(self.FORCE_WIKI_UPDATE_FILEPATH):
                    log('Forcing wiki update')
                    handler.update()
                    os.remove(self.FORCE_WIKI_UPDATE_FILEPATH)
                    log('Done updating wiki')
                if handler:
                    handler.process(post)
                self.mark_checked(post)

    def scan_forever(self, handler: PostHandler):
        print('running')
        while True:
            try:
                self.scan(handler)
            except Exception as e:
                log(str(e))
                traceback.print_stack(e)
                sleep(60)
                log('restarting now')
