from django.contrib import admin

from core.main.models import Problem, Rate, SolutionResult, TestCase

# Register your models here.
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Rate)
admin.site.register(SolutionResult)