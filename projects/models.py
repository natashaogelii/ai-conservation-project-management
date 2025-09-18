from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Project(models.Model):
    DEPARTMENTS = [
        ("Wildlife", "Wildlife Protection"),
        ("Rangelands", "Rangelands"),
        ("Invasive", "Invasive Species"),
        ("Water", "Water Catchment"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Use through for advanced team membership
    team_members = models.ManyToManyField(
        User,
        through="ProjectTeamMembership",
        related_name="projects"
    )

    def __str__(self):
        return self.title

    @property
    def total_spent(self):
        return sum(exp.amount for exp in self.expenses.all())

    @property
    def remaining_budget(self):
        return self.budget - self.total_spent

    @property
    def progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(completed=True).count()
        return int((completed_tasks / total_tasks) * 100)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.project.title})"


class ExpenditureLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses")
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.amount}"


class ProjectTeamMembership(models.Model):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("developer", "Developer"),
        ("researcher", "Researcher"),
        ("assistant", "Assistant"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"
