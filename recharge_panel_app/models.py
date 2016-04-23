from django.db import models

# Create your models here.


class CreateUser(models.Model):
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email_id = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    address = models.CharField(max_length=30)

    def __repr__(self):
        return self.name
