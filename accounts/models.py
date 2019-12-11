from django.db import models
from django.contrib.auth.models import AbstractUser
#from PIL import Image
#from imagekit.models import ProcessedImageField
#from imagekit.processors import ResizeToFill


class CustomUser(AbstractUser):
  """ The custom user model modifies the email field to be unique for all users """
  email = models.EmailField(unique=True)

  def __str__(self):
    return self.email


# class Profile(models.Model):
#   """ Profile for user. It has an one-to-one relationship with its respective
#   user """
#   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#   picture = ProcessedImageField(default='default.jpg', upload_to='profile_pics',
#                                 null=True, processors=[ResizeToFill(125, 125)],
#                                 format='JPEG',
#                                 options={'quality': 99})

#   def __str__(self):
#     return f'{self.user.username} profile'
