# -*- coding: utf-8 -*-

from plugins.Plugin import *
import re
import string
import tweepy

class TwitterPlugin(Plugin):
    name = "TwitterPlugin"
    author = "Olle@Johansson.com"
    description = "Posts all messages to Twitter."
    commands = [
        dict(
            command = [''],
            handler = 'tweet_post',
            onevents = ['Message', 'SentMessage'],
        )
    ]
    ignored_names = ['HALiBot']
    max_name_len = 4

    def setup(self):
        """
        Setup the Twitter authentication.
        """
        # Setup Twitter connection.
        auth = tweepy.OAuthHandler(self.bridge.cfg.get('twitter_consumer_key'), self.bridge.cfg.get('twitter_consumer_secret'))
        auth.set_access_token(self.bridge.cfg.get('twitter_oauth_token'), self.bridge.cfg.get('twitter_oauth_token_secret'))
        self.twit = tweepy.API(auth)

        # Compile regular expressions for name shorteing.
        self.re_sc = re.compile(r"[\W_-]", re.UNICODE)
        self.re_sp = re.compile(r"\s+", re.UNICODE)
        self.re_up = re.compile(r"[A-ZÅÄÖÛŒÆ]", re.UNICODE)
        self.re_fl = re.compile(r"((?<=\A).|(?<= )[A-ZÅÄÖÛŒÆ])", re.UNICODE)

    def tweet_post(self, shout, command, comobj):
        """
        Post shout message to Twitter.
        """
        name = self.shorten_name(shout.name)
        text = self.shorten_text(shout.text, 140 - len(name) - 2)
        status = u'%s ^%s' % (text, name)
        self.logprint("Tweeting:", status)
        self.twit.update_status(status)

    def shorten_text(self, text, length):
        """
        Shorten text to given length.
        """
        if len(text) <= length:
            return text
        return text[:length-1] + u"…"

    def shorten_name(self, name):
        initials = ''

        # Don't shorten some names.
        if name in self.ignored_names:
            return name

        # Remove anything that isn't a word character.
        name = self.re_sc.sub(' ', name)

        # Only keep one consecutive space
        name = self.re_sp.sub(' ', name)
        name = string.strip(name)

        # If string has spaces, take first letter in each word and return
        if string.find(name, ' ') >= 0:
            initials = self.re_fl.findall(name)
            if initials:
                return ''.join(initials)

        # If name is shorter than a set length, just return it.
        if len(name) <= self.max_name_len:
            return name
        
        # Else get all upper case letters
        initials = self.re_up.findall(name)
        if initials:
            initials = ''.join(initials)

        # If string is same as input, or empty, just take first letter.
        if not initials or initials == name:
            return name[0:1]

        return initials

if __name__ == "__main__":
    print shorten_text("1234567890", 8)
    print shorten_name("Olle Johansson")
    print shorten_name("Gardener")
    print shorten_name("krank")
    print shorten_name("Tony.M.Meijer")
    print shorten_name("Jesus H. Christ")
    print shorten_name("McFisk")
    print shorten_name("HALiBot")
    print shorten_name("Johan K")
    print shorten_name("_-olle-_")
    print shorten_name("BOSSE")
