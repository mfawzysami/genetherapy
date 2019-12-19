from utils.logs import log
from utils.config import EnvironmentManager
import pyotp as otp
import base64
from users.models import User


class AccountTokenManager:
    def __init__(self):
        self.env = EnvironmentManager()

    def generateExternalLink(self,username,otp,config_param):
        try:
            if not username or not otp:
                raise Exception("username can't be none")
            site_url = self.env.get_item('general','site_url')
            token = "{0}:{1}".format(username,otp)
            full_url = "{0}{1}?code={2}".format(site_url,config_param,base64.encodestring(token))
            return full_url

        except Exception as e:
            print (e.message)
            log.error(msg=e.message)
            return None

    def generateExternalLink_forfile_user(self, username, filename):
        try:
            if not username:
                raise Exception("username can't be none")

            site_url = self.env.get_item('general','site_url')
            portal_url = self.env.get_item('general','portal_url')
            error_upload = self.env.get_item('general','error_upload')
            full_url = "{0}/{1}/{2}/?file={3}".format(site_url,portal_url,error_upload,filename)
            return full_url

        except Exception as e:
            print (e.message)
            log.error(msg=e.message)
            return None


    def generate_temporary_token(self,secret):
        otp_interval = self.env.get_item('security','otp_interval')
        otp_manager = otp.TOTP(secret, interval=int(otp_interval))
        otp_value = otp_manager.now()
        return otp_value



    def verify_link_token(self,link_token):
        otp_interval = self.env.get_item('security', 'otp_interval')
        base64_decoded = base64.decodestring(link_token)
        if not ':' in base64_decoded:
            raise Exception("Invalid Link Token Sent - Unable to verify the link")
        username , otpValue = base64_decoded.split(':')
        current_user = User.objects.filter(username=username).first()
        if not current_user:
            raise Exception("Invalid Activation Link Sent - Unable to verify the link")
        if not int(current_user.secret_otp) == int(otpValue):
            raise Exception("Invalid Activation Link Sent - Unable to verify the link")
        secret_hash = current_user.secret_hash
        otp_manager = otp.TOTP(secret_hash, interval=int(otp_interval))
        return otp_manager.verify(otpValue) , username

    def get_username_from_token(self,link_token):
        base64_decoded = base64.decodestring(link_token)
        if not ':' in base64_decoded:
            raise Exception("Invalid Link Token Sent - Unable to verify the link")
        username, otpValue = base64_decoded.split(':')
        return username






