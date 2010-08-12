# -*- coding: utf-8 -*-

from plugins.Plugin import *

class TwitterPlugin(Plugin):
    name = "TwitterPlugin"
    author = "Olle@Johansson.com"
    description = "Posts all messages to Twitter."
    commands = [
        dict(
            command = [''],
            handler = 'tweet_post',
            onevents = ['Message'],
        )
    ]

    def tweet_post(self, shout, command, comobj):
        tweeturl = "http://api.twitter.com/1/statuses/update.json"
        result = loadUrl(tweeturl, method="POST", params=dict({
            'status': '%s ^%s' % (shout.text, shout.name),
        }), auth=dict({
            'realm': 'Twitter API',
            'uri': tweeturl,
            'user': self.bridge.cfg.get('twitter_user'),
            'password': self.bridge.cfg.get('twitter_password'),
        }))

