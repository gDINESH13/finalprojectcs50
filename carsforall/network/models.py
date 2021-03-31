from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass
    




class Car(models.Model):
	owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cars_owned")
	name=models.CharField(max_length=100)
	description=models.CharField(max_length=500)
	no_plate=models.CharField(max_length=50)
	posted_on=models.DateTimeField()
	image=models.URLField(default=None)
	rent=models.IntegerField()
	seats=models.IntegerField()
	status=models.BooleanField(default=True)
	insurance=models.BooleanField(default=True)
	dents=models.BooleanField(default=True)
	subscribers=models.ManyToManyField(User,blank=True,related_name="wishlist")
	renters_wished=models.ManyToManyField(User,blank=True,related_name="asked_for_rent")
	#past_renters=models.ManyToManyField(User,blank=True,related_name="rented")
	current_renter=models.ManyToManyField(User,blank=True,related_name="currenly_rented")
	curr_time_rent=models.DateTimeField(blank=True,editable=True)

	def __str__(self):
		return f"owner:{self.owner} carname:{self.name} rent:{self.rent}"



class History(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="carsRentedSoFar")
	car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="usersRentedSoFar")
	time_of_rent=models.DateTimeField()
	time_of_endrent=models.DateTimeField(blank=True)

	def __str__(self):
		return f"{self.user} has rented {self.car}"
