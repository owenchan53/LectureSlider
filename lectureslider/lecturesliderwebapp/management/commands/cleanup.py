from django.core.management.base import BaseCommand
from django.conf import settings
import os
from os.path import join, exists
from lecturesliderwebapp.models import Video

class Command(BaseCommand):
    help = 'Deletes video files that are no longer referenced in the database'

    def handle(self, *args, **options):
        files_in_database = [video.vid_file.name for video in Video.objects.all()]
        files_on_disk = os.listdir(settings.MEDIA_ROOT + '/videos/')
        
        for file_name in files_on_disk:
            if file_name not in files_in_database:
                file_path = join(settings.MEDIA_ROOT, 'videos', file_name)
                if exists(file_path):
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted {file_path}'))