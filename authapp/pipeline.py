import datetime
import urllib
from urllib.request import urlopen

import requests
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max&access_token={response['access_token']}&v=5.92"

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    print(resp.json())

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = datetime.datetime.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_max']:
        img_url = data['photo_max']
        img = urllib.request.urlopen(img_url).read()
        out = open('media/users_avatars/vk.jpg', 'wb')
        out.write(img)
        out.close()
        img = 'users_avatars/vk.jpg'
        user.avatar = img

    user.save()
