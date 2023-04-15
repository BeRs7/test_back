from users.models import User
from utils.filters import BaseFilter


class CRMUsersFilter(BaseFilter):
    searching_fields = ("id", "email", "first_name", "last_name", "phone_number")

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number"]
