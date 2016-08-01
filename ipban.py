#-*- coding: UTF-8 -*-
#/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import logging

import webapp2
from google.appengine.api import urlfetch

import json
import random

FBtoken = "Fan book Token Here"

ResponsePattern = [
    u'太強啦',
    u'太神啦',
    u'太狂啦',
    u'太猛啦',
    u'太潮啦',
    u'worship',
    u'大大太強了',
    u'為什麼你可以這麼厲害',
    u'太強了我要跪了',
    u'看來我還是去吃土吧',
    u'太強啦RRRRRRR',
    u'(worship)']


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("Hello, World!")


class FBwebhook(webapp2.RequestHandler):
    def send_fb_message(self, to, message):
        post_url = "https://graph.facebook.com/v2.6/me/messages?access_token={token}".format(
                token=FBtoken)
        response_message = json.dumps(
            {"recipient": {"id": to},
             "message": {"text": message}})
        logging.info(post_url)
        logging.info(response_message)
        result = urlfetch.fetch(
                url=post_url,
                headers={"Content-Type": "application/json"},
                payload=response_message,
                method=urlfetch.POST)

        logging.info("[{}] reply to {}: {}".format(
            result, to.encode('utf-8'), message))

    def get(self):
        verification_code = "IPBanIsTheWeakestPersonInTheWorld"
        verify_token = self.request.get('hub.verify_token')
        verify_challenge = self.request.get('hub.challenge')
        if verification_code == verify_token:
            self.response.write(verify_challenge)
        else:
            self.response.write("Error, wrong validation token")

    def post(self):
        logging.info(self.request.body)
        message_entry = json.loads(self.request.body)['entry']

        for entry in message_entry:
            messagings = entry['messaging']
            for message in messagings:
                sender = message['sender']['id']
                if message.get('message'):
                    text = message['message']['text'].encode('utf-8')
                    logging.info(u"{} says {}".format(sender, text))

                message = random.choice(ResponsePattern).encode('utf-8')
                logging.info(message)
                self.send_fb_message(sender, message)


app = webapp2.WSGIApplication([
    ('/webhook', FBwebhook),
    ('/', MainPage),
], debug=True)
