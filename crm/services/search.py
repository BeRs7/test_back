from typing import Dict, List, Any

from django.apps import apps
from django.db.models import Q, CharField, TextField, PositiveSmallIntegerField
from django.forms import EmailField, IntegerField

from catalog.models import Product, Category
from orders.models import Order
from users.models import User


class GlobalSearch:
    ProductTranslation = apps.get_model("catalog", "ProductTranslation")
    CategoryTranslation = apps.get_model("catalog", "CategoryTranslation")
    models = [User, ProductTranslation, CategoryTranslation, Product, Category, Order]

    @staticmethod
    def _serialize_objects(models: list) -> List[Dict[str, str]]:
        json_data = []
        for model in models:
            for qs in model:
                json_data.append(
                    {
                        "id": qs.id,
                        "type": qs._meta.verbose_name,
                        "name": str(qs),
                        "detail_url": qs.get_crm_detail_url(),
                    }
                )
        return json_data

    def search(self, search_query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Make a search through few models
        @param search_query:
        @return: list
        """
        search_results = []
        for model in self.models:
            # map all text fields in model
            fields = [
                x
                for x in model._meta.get_fields()
                if isinstance(x, (CharField, TextField, EmailField, IntegerField, PositiveSmallIntegerField))
            ]
            search_queries = [Q(**{x.name + "__icontains": search_query}) for x in fields]
            q_object = Q()
            for query in search_queries:
                q_object = q_object | query

            results = model.objects.filter(q_object).distinct()
            if results:
                # If there are search objects, try to get original obj, not TranslatedModel
                try:
                    search_results.append([result.master for result in results])
                except AttributeError:
                    search_results.append(results)
        return {"results": self._serialize_objects(search_results)}
