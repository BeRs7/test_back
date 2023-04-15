from django.forms import ModelForm

from orders.models import RegistrationForFitting
from utils.forms import StyledForm


class RegistrationForFittingUpdateForm(StyledForm, ModelForm):

    class Meta:
        model = RegistrationForFitting
        fields = (
            "full_name",
            "phone",
            "email",
            "date_of_wedding",
            "comment",
            "time",
            "service_type",
            "external_id",
            "external_hash",
        )
