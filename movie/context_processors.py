from . models import *


def profilePic(request):
    if request.user.is_authenticated:
        context = {'profile': Profile.objects.get(user=request.user), 
                    'latest_news': Blog.objects.all()}
    else:
        context = {'profile': None,
                    'latest_news': Blog.objects.all()}
    return context