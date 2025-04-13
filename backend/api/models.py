from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    variations = models.CharField(max_length=255)
    layout = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    startsAt = models.DateTimeField()
    endsAt = models.DateTimeField()
    permalink = models.CharField(max_length=255)
    price = models.IntegerField()
    razorpay_Id = models.CharField(max_length=255)

    def __str__(self):
        return self.title

#might be required later to track payments  
# class PaymentField(models.Model):
#     eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
#     price = models.IntegerField()
#     razorpay_Id = models.CharField(max_length=255)

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Will store hashed password
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email