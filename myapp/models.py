from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tasks(models.Model):
    task_name = models.CharField(max_length=50)
    task_url = models.URLField (max_length=200)
    category = models.CharField(max_length=50, default="Others")
    task_ss = models.ImageField(upload_to='task_ss/')
    points = models.IntegerField()

    def __str__(self):
        p = str(self.task_name) + ',' + str(self.points)
        return (p)


class CompletedTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    completed_task_ss = models.ImageField(upload_to='completed_task_ss/')
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        p = str(self.user) + ',' + str(self.task) + ',' + str(self.completed_at)
        return (p)
