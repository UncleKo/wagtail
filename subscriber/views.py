from django.shortcuts import render
from .models import Subscriber
from django.views.generic import CreateView


class SubscriberCreateView(CreateView):
  model = Subscriber
  fields = '__all__'
  success_url = '/'
