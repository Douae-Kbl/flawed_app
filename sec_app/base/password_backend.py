
#FLAW 5 A02:2021-Cryptographic Failures

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class passwordbackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
