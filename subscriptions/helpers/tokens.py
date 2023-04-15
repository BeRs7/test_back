import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SubscribeEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, subscription, timestamp):
        return six.text_type(subscription.email) + six.text_type(timestamp) + six.text_type(subscription.is_active)


subscribe_activation_token = SubscribeEmailTokenGenerator()
