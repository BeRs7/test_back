from typing import List


class SubscriptionHelper:
    """
    Group actions on subscriptions list
    """

    def __init__(self, instance):
        super().__init__()
        self.instance = instance

    def disable_subscriptions(self, ids: List[int]):
        return self.instance.objects.filter(id__in=ids).update(is_active=False)

    def enable_subscriptions(self, ids: List[int]):
        return self.instance.objects.filter(id__in=ids).update(is_active=True)

    def delete_subscriptions(self, ids: List[int]):
        return self.instance.objects.filter(id__in=ids).delete()

    def copy_subscriptions(self, ids: List[int]):
        for subscription in self.instance.objects.filter(id__in=ids):
            subscription.id = None
            subscription.is_active = False
            subscription.save()
