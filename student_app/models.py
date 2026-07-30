from django.db import models


class Student(models.Model):
    student_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=150)
    branch = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.student_name
