""" Created Sat Sep 14 2013 by Tristan Trim... lulz.

This is avatarBot, it manages avatars. When you call with a user and a size, it returns: thumbnail, picture, renderType.

That is all. """


from django.contrib.auth.models import User
from avatarBot.models import uploadPic, userPicThumb


###	This main function here calls the function of whatever user.avatarType is	###
def getPic(user, size):

    return eval(user.profile.avatarType)(user, size)


def upload(user, size):

    userpic = uploadPic.objects.filter(user = user)[0]

    thumbpic = userPicThumb.objects.get_or_create(pic = userpic, filex = size[0], filey = size[1])[0]

    return thumbpic.thumb.url, userpic.filename.url, userpic.profilePicType


def default(user, size):

    thumbpic = "noUserPic.png"

    userpic = "noUserPic.png"

    return "/static/noUserPic.png", "/static/noUserPic.png", "browser"
