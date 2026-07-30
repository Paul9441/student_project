from django.urls import path
from . import views


urlpatterns = [

    path('students/',views.students,name='students'),

    path(
        'students/<int:id>/',
        views.student_detail,
        name='student_detail'
    ),

    path(
        'students/<int:id>/update/',
        views.update_student,
        name='update_student'
    ),

    path(
        'students/<int:id>/delete/',
        views.delete_student,
        name='delete_student'
    ),
]

