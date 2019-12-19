import os
from django.conf import settings
from configparser import ConfigParser


class EnvironmentManager(object):
    def __init__(self):
        """ Get the environment variables """
        self.ini_path = os.path.join(settings.BASE_DIR,"genetherapy.ini")
        """Read the configuration path into config Parser"""
        self.configReader = ConfigParser()
        self.configReader.read(self.ini_path)

    def getValueForSectionAndKey(self, sectionName, keyName):
        if self.configReader is None:
            return None
        else:
            try:
                return self.configReader.get(sectionName, keyName)
            except Exception:
                return None

    def get_item(self,section,key):
        return self.getValueForSectionAndKey(section,key)


