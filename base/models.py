


# this is where we are going to create our database tables
# mostly about user and their actions in the web
# this has to be in the form of classes due to many functionalty


from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio =models.TextField(null=True)
    
    avatar = models.ImageField(null=True, default="avatar.png")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# this for the topics

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
# this is for the rooms
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
 
    
 # class for ordering the time room like ordering them depending on the thme they were created
 
 
    class Meta:
       ordering = ['-update', '-created']
    
   
    
    # then add this class function to call out the datas on the database
    def __str__(self):
        return self.name
    

    # each room should have a message
    

# this is for messages    
class Message(models.Model):
    
        # for specifing rooms of many to one
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
       ordering = ['-update', '-created']
    
   
        
    def __str__(self):
        return self.body[0:50]
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    