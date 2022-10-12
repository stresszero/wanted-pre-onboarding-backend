from django.urls import path

from .views import create_job_posting, JobPostingView, get_job_postings, user_job_apply

urlpatterns = [
    path('', create_job_posting),
    path('/list', get_job_postings),
    path('/<int:posting_id>', JobPostingView.as_view()),
    path('/<int:posting_id>/apply', user_job_apply),
]