from django.contrib import admin
from .models import Item

# Register your models here.

@admin.register(Item)
class QuestionAdmin(admin.ModelAdmin):
    pass
