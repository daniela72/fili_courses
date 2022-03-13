from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # name index is taken from {% url 'courses:index' %}
    # path('', views.index, name='index'),
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    # path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    # ex: course/5/
    path('grade/<int:course_id>/', views.course_details, name='course_details'),
    # route to start the test view
    path('grade/<int:course_id>/test/<int:lesson_id>/', views.start_test, name='start_test'),
    path('grade/<int:course_id>/submit_test/<int:lesson_id>/', views.submit_test, name='submit_course_test'),
    # route for show_exam_result view
    path('result/<int:course_id>/<int:lesson_id>/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)