from django.contrib import admin
from .models import Question, Answer


admin.site.register(Answer)


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
