from django.db import models

# Create your models here.
class Video(models.Model):
    name= models.CharField(max_length=500)
    vid_file= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.vid_file)