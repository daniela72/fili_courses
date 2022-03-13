from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Course, Lesson, Choice, Question, Submission
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import logging
from django.urls import reverse
from django.views import generic
# Get an instance of a logger
logger = logging.getLogger(__name__)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        # remove courses/ and works
        # link displays registration only. Not user_registration_bootstrap.html
        return render(request, 'user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("courses:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('courses:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'user_login_bootstrap.html', context)
    else:
        return render(request, 'user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('courses:index')


'''
def index(request):
    # Before was return HttpResponse('Hello FiliCourses')
    # return all the courses from Model Course in the database
    courses = Course.objects.all()
    # the third argument is a dictionary. This dictionary is called the context.
    # It provides data to use in a template.
    # The property called 'courses' can be accessed in the template by looping with courses
    return render(request, 'index.html', {'courses': courses})
'''


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        # return all the courses from Model Course in the database
        courses = Course.objects.all()
        return courses


'''
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course_details.html'

'''


def course_details(request, course_id):
    '''
    https://stackoverflow.com/questions/19336076/django-reverse-for-detail-with-arguments-and-keyword-arguments-n
    '''
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course_details.html', {'course': course})


def start_test(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    # pass course_id
    context = {}
    context['lesson'] = lesson
    context['course_id'] = course_id
    return render(request, 'course_test.html', context)


# Create a submit view to create an exam submission record
def submit_test(request, course_id, lesson_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    question = get_object_or_404(Question, pk=lesson_id)
    # user = request.user
    # enrollment = Enrollment.objects.get( course=course)
    # question=question is in the Submission model
    submission = Submission.objects.create(question=question)

    answers = extract_answers(request)
    for answer in answers:
        each_answer = Choice.objects.filter(id=int(answer)).get()
        submission.choices.add(each_answer)
    submission.save()

    return HttpResponseRedirect(reverse(viewname='courses:show_exam_result', args=(course_id, lesson_id, submission.id,)))


# Method to collect the selected choices from the exam form from the request object
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        # key in post
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers


# Create an exam result view to check if learner passed exam
def show_exam_result(request, course_id, lesson_id, submission_id):
    course = Course.objects.get(pk=course_id)
    lesson = Lesson.objects.get(pk=lesson_id)
    submission = Submission.objects.get(pk=submission_id)
    selected_ids = []
    not_selected = []
    grade = 0
    submission_choices_ids = submission.choices.values_list('pk', flat=True)

    for question in lesson.question_set.all():
        total_question = lesson.question_set.all().count()
        question.not_selected(submission_choices_ids, not_selected)
        if question.is_get_score(submission_choices_ids):
            # total grade for each question
            grade += question.grade

    # choice in exam_result_bootstrap
    for choice in submission.choices.all():
        selected_ids.append(choice.id)

    context = {}
    context['course'] = course
    context['lesson'] = lesson
    context['selected_ids'] = selected_ids
    context['grade'] = int(100 * grade / total_question)
    return render(request, 'exam_result.html', context)

