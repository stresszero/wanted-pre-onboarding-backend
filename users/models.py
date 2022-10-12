from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


class UserJobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey("postings.JobPosting", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_job_applications"

    def __str__(self):
        return self.user.name
