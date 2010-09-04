# -*- coding: utf-8 -*-

from plugins.Plugin import *
from utils.MixIn import *
import re
import string
import tweepy
from datetime import datetime, date, time, timedelta
from twisted.internet import task
from twisted.internet import reactor

# TODO:
# Setup a reactor in setup to call handle_mentions instead of calling it on tweets.
# Fix looping issue, possible only push out messages starting with account name and removing it.

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
    latest_id = 0

    def setup(self):
        """
        Setup the Twitter authentication.
        """
        # Setup Twitter connection.
        auth = tweepy.OAuthHandler(self.bridge.cfg.get('twitter_consumer_key'), self.bridge.cfg.get('twitter_consumer_secret'))
        auth.set_access_token(self.bridge.cfg.get('twitter_oauth_token'), self.bridge.cfg.get('twitter_oauth_token_secret'))
        self.twit = tweepy.API(auth)

        # Start listening to Twitter mentions.
        utime = float(self.bridge.cfg.get('twitter_update_time'))
        if utime:
            l = task.LoopingCall(self.handle_mentions)
            d1 = l.start(utime)

        # Compile regular expressions for name shorteing.
        self.re_sc = re.compile(r"[\W_-]", re.UNICODE)
        self.re_sp = re.compile(r"\s+", re.UNICODE)
        self.re_up = re.compile(u"[A-ZÅÄÖÛŒÆ]", re.UNICODE)
        self.re_fl = re.compile(u"((?<=\\A).|(?<= )[A-ZÅÄÖÛŒÆ])", re.UNICODE)

    def tweet_post(self, shout, command, comobj):
        """
        Post shout message to Twitter.
        """
        name = self.shorten_name(shout.name)
        text = self.shorten_text(shout.text, 140 - len(name) - 2)
        status = u'%s ^%s' % (text, name)
        #self.logprint("Tweeting:", status)
        try:
            self.twit.update_status(status)
        except tweepy.TweepError, te:
            self.logprint('Twitter raised an exception:', te)

    def handle_mentions(self):
        """
        Load mentions from Twitter and send them to Jabber and Shoutbox if they fulfill the criterias.
        """
        #self.logprint('handle_mentions')
        if not self.bridge.xmlstream:
            self.logprint("Twitter plugin can't handle mentions yet since there is no xmlstream.")
            return
        self.latest_id = self.latest_id or self.bridge.db.get_value('twitter_latest_mention_id')
        #self.logprint("Latest id was:", self.latest_id)
        if self.latest_id:
            mentions = self.twit.mentions(self.latest_id)
        else:
            mentions = self.twit.mentions()
        for tweet in mentions:
            self.logprint('Found mention on Twitter:', tweet.user.screen_name, tweet.text)
            if tweet.id > self.latest_id:
                self.latest_id = tweet.id
            self.handle_tweet(tweet)
        self.bridge.db.set_value('twitter_latest_mention_id', self.latest_id)
        #self.logprint("Updated latest_id to:", self.latest_id)

    def handle_tweet(self, tweet):
        # Ignore own tweets.
        my_name = self.twit.me().screen_name
        starttext = '@%s ' % my_name

        # Skip tweets from own account.
        if tweet.user.screen_name == my_name:
            #print "screen_name = my_name", tweet.user.screen_name, my_name
            return

        # Skip tweets that doesn't start with own screen_name
        if not tweet.text.startswith(starttext):
            #print "doesn't start with", starttext
            return

        text = self.strip_command(tweet.text, starttext)
        self.bridge.send_and_shout(text, '@%s' % tweet.user.screen_name)

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
