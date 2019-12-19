import urllib
import urllib2
import json
from genetherapy import settings

def validate_recaptcha(g_recaptcha_response):
    url = settings.RECAPTCHA_VERIFICATION_URL
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': g_recaptcha_response
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    result = json.load(response)
    if result and result['success']:
        return True
    else:
        return False
