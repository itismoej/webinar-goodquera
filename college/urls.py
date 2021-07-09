from django.urls import path

from college.views import (
    CollegeDetailView, CollegesView, LessonDetailView, LessonsView, CollegeRegister
)

urlpatterns = [
    path(
        'colleges/',
        CollegesView.as_view(),
        name='colleges',
    ),
    path(
        'colleges/<int:college_id>/',
        CollegeDetailView.as_view(),
        name='college-detail'
    ),
    path(
        'colleges/<int:college_id>/register/',
        CollegeRegister.as_view(),
        name='join-college'
    ),
    path(
        'colleges/<int:college_id>/lessons/',
        LessonsView.as_view(),
        name='lessons'
    ),
    path(
        'colleges/<int:college_id>/lessons/<int:lesson_id>/',
        LessonDetailView.as_view(),
        name='lesson-detail'
    ),
]
