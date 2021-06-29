from django.core.management.base import BaseCommand
from os import mkdir, path
from django.conf import settings

class Command(BaseCommand):
    """
    """

    def handle(self, *args, **kwargs):
        required_dirs = [
            "cards",
            "reports"
        ] 

        try:        
            for dir in required_dirs:
                new_media_dir = "{0}/{1}".format(settings.MEDIA_ROOT, dir)
                if not path.isdir(new_media_dir):
                    print(new_media_dir)
                    mkdir(new_media_dir)
        except:
            raise Exception("Error during media directories creation")
        else:
            print("Finish creating media dirs")