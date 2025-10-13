from .models import Question
from .models import Person
from django.contrib import admin

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    # pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ["shirt_size", ("first_name", "last_name")]
    empty_value_display = "-empty-"

# @admin.register(Question, Person)
# class QuestionAdmin(admin.ModelAdmin):
#     date_hierarchy = "pub_date"

# admin.site.register(Question)
# admin.site.register(Person)
