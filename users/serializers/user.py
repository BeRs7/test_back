from rest_framework import serializers

from catalog.models import Product


class ToggleUserFavoriteSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    exists_in_favorites = serializers.BooleanField(read_only=True, allow_null=True, required=False)

    def create(self, validated_data=None):
        favorites_list = (
            self.context["request"].session.get("favorites")
            if self.context["request"].session.get("favorites")
            else []
        )
        product = self.validated_data["product"]  # type: Product
        self.validated_data["exists_in_favorites"] = product.id in favorites_list
        if self.validated_data["exists_in_favorites"]:
            favorites_list.remove(product.id)
            self.context["request"].session["favorites"] = favorites_list
        else:
            favorites_list.append(product.id)
            self.context["request"].session["favorites"] = favorites_list

        return product

    @property
    def data(self):
        return {
            "product": self.validated_data["product"].id,
            "exists_in_favorites": not self.validated_data["exists_in_favorites"],
        }
