from django.db.models.signals  import pre_save
from django.contrib.auth.models import User

def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email

pre_save.connect(updateUser, sender=User)

#User experience intuition: I want to use email as their login username they dont have remember different credential. Therefore, I used django signals, technically speaking when the User changes their email address this will fire off a function to update the username as well. If the email is not empty, then take email and update the username and pass in the user.email
