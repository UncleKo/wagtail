from django import forms
from .models import Subscriber

class SubscriberCreateForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        fields = '__all__'