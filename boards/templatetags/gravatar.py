from django import template
import  hashlib
from  urllib.parse import urlencode
from django.conf import  settings


register = template.Library()


@register.filter
def	gravatar(user):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size  = 120
    url =  "http://www.gravatar.com/avatar/{md5}?{params}".format(
        md5 = hashlib.md5(email).hexdigest(),
        params = urlencode({'d':default,'s':size})
    )
    return url