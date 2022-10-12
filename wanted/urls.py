from django.urls import path, include

urlpatterns = [
    path("postings", include("postings.urls")),
]
