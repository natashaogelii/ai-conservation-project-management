from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    DEPARTMENTS = [
        ("Wildlife", "Wildlife Protection"),
        ("Rangelands", "Rangelands"),
        ("Invasive", "Invasive Species"),
        ("Water", "Water Catchment"),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Create your models here.
