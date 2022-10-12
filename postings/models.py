from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = "areas"

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name="job_postings"
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=100)
    reward = models.PositiveIntegerField(default=0)
    tech = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = "job_postings"
