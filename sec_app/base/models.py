from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#create our database basically

class task(models.Model):
    user= models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True)#one to many reltshp
    title= models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    complete= models.BooleanField(default=False)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:#to order list so that the complete ones are at the bottom
        ordering=['complete']

    #hen you run migration it means that itprepares how to create the sql tables and migrate provides an sql table has been created for this model