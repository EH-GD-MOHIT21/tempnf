'''
Caching of otps/verification Related
queries will be available here
'''
from random import randint,choice
from django.core.cache import cache
from django.conf import settings

def set_cache(data,otp):
    obj = {
        "first_name":data["first_name"],
        "last_name":data["last_name"],
        "password":data["password"],
        "otp":otp
    }
    cache.set(data["email"],obj,timeout=300)


def Fetch_cache(email):
    value = cache.get(email)
    if value == None:
        raise ValueError("User Does Not Exists.")
    return value



def GenerateOTP():
    return randint(100000,999999)


def GenerateSlug(length=None):
    if length == None:
        length = 50
    chars = settings.VALID_CHARS
    slug = ''
    for i in range(length):
        slug += choice(chars)
    return slug


def delete_pattern(email):
    for key in cache._cache.keys():
        tk = key.split(':')[2]
        if tk == email:
            del cache._cache[key]