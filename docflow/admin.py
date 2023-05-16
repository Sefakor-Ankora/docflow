from django.contrib import admin
from .models import Project, BudgetLine, Memo, LeaveRequest, Notification


# Register your models here.
admin.site.register(Memo)
admin.site.register(LeaveRequest)
admin.site.register(Notification)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    #Creating project lines
    project1 = Project.objects.create(name='Project 1')
    project2 = Project.objects.create(name='Project 2')


@admin.register(BudgetLine)
class BudgetLineAdmin(admin.ModelAdmin):
    # Creating budget lines
    budget_line1 = BudgetLine.objects.create(name='Budget Line 1')
    budget_line2 = BudgetLine.objects.create(name='Budget Line 2')



