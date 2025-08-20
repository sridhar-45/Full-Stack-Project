from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)   #  ✅ multiple codes allowed
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
