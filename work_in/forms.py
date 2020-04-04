from django.db import models
from django.forms import ModelForm
from appModel.models import Table

class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = "__all__"
        labels = {
            'space': 'ความจุ ',
            'status': 'สถานะ '
        }