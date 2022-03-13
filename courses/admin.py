from django.contrib import admin
# the period on .models means 'in the current folder'
from .models import Course, Instructor, Lesson, Question, Choice, Submission
# dany marisa
# localhost:8000/admin/


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


# convention to follow Courses+Admin
# inherit the class ModelAdmin from the module admin -> admin.ModelAdmin
class CourseAdmin(admin.ModelAdmin):
    # here we can override or change some of the attributes to display for example
    # we choose what we want to display in the admin area
    list_display = ('name', 'description')


class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_time')


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "order", "course", "content")


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "grade", "lesson")


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")


# register the models you want to manage in the Admin area.
# The first argument will make the model Course available on the Admin area
# The second argument -> CourseAdmin will tell Django how to present the model Course
admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission)
