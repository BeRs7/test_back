from typing import List

from users.models import User


class UserHelper:
    """
    Group actions on users list
    """

    def delete_users(self, ids: List[int]):
        return User.objects.filter(id__in=ids).delete()

    def copy_users(self, ids: List[int]):
        for user in User.objects.filter(id__in=ids):
            user.id = None
            user.save()
