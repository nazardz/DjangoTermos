from django.contrib import admin
from .models import *

model_list = [
	Post,
	Station,
]

admin.site.register(model_list)

