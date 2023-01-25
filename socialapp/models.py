from django.db import models

# Create your models here.


from django.contrib.auth.models import User


class Post(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_date=models.DateField(auto_now_add=True)
    upvote=models.ManyToManyField(User,related_name="upvote")
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.title



class Comment(models.Model):
    title=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_date=models.DateField(auto_now_add=True)
    



    def __str__(self):
        return self.comment
