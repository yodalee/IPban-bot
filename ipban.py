import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("Hello, World!")


class FBwebhook(webapp2.RequestHandler):
    def get(self):
        verification_code = "Verification code"
        verify_token = self.request.get('hub.verify_token')
        verify_challenge = self.request.get('hub.challenge')
        if verification_code == verify_token:
            self.response.write(verify_challenge)
        else:
            self.response.write("Error, wrong validation token")


app = webapp2.WSGIApplication([
    ('/webhook', FBwebhook),
    ('/', MainPage),
], debug=True)
