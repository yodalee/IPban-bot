import webapp2
import json
from google.appengine.api import urlfetch


FBtoken = "Fan book Token Here"


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
        print(post_url)
        print(response_message)
        result = urlfetch.fetch(
                url=post_url,
                headers={"Content-Type": "application/json"},
                payload=response_message,
                method=urlfetch.POST)

        print("[{}] reply to {}: {}".format(result, to, message))

    def get(self):
        verification_code = "Verification code"
        verify_token = self.request.get('hub.verify_token')
        verify_challenge = self.request.get('hub.challenge')
        if verification_code == verify_token:
            self.response.write(verify_challenge)
        else:
            self.response.write("Error, wrong validation token")

    def post(self):
        print(self.request.body)
        message_entry = json.loads(self.request.body)['entry']

        for entry in message_entry:
            messagings = entry['messaging']
            for message in messagings:
                sender = message['sender']['id']
                if message.get('message'):
                    text = message['message']['text']
                    print("{} says {}".format(sender, text))
                self.send_fb_message(sender, "Hi")


app = webapp2.WSGIApplication([
    ('/webhook', FBwebhook),
    ('/', MainPage),
], debug=True)
