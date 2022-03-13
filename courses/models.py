import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading Django modules. Do you have Django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


# grade / courses
class Course(models.Model):
    name = models.CharField(max_length=30, default='Course/Grade')
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=2083)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# lesson / list of test options
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    # for the admin. Returns the title lesson
    def __str__(self):
        return self.title


# Create a Question Model
class Question(models.Model):
    question_text = models.CharField(max_length=200, default="Question")
    grade = models.IntegerField(default=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    # for the admin. Return the question
    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_wrong = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()

        if all_answers == selected_correct and selected_wrong == 0:
            return True
        else:
            return False

    def not_selected(self, selected_ids, not_selected):
        missing = self.choice_set.filter(is_correct=True).exclude(id__in=selected_ids)
        for el in missing:
            not_selected.append(el)


#  Create a Choice Model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=True)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f'{self.question} {self.choices}'


