from django.db import models
from django.contrib.auth.models import User

class Movie(models.Models):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to="movies/")
    rating=models.DecimalField(max_digits=3,decimal_place=1)
    cast=models.textField()
    description=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.name
    
class Theater(models.Models):
    name=models.CharField(max_length=255) 
    movie=models.Foreignkey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time=models.DateTimeField()
    
    def __str__(self):
        return f'{self.name} -{self.movie,name}  at {self.time}'
    
class Seat(models.Model):
    Theater=models.Foreignkey(Theater,on_delete=models.CASCADE,related_name='seats') 
    seat_number=models.models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'
    
class Booking(models.Models):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie=models.ForeignKey(User,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_date=models.CASCADE) 
    bookrd_at=models.DateTimeField(auto_noe_add=True)
    
    def __str__(self):
        return f'Booking by{self.user.username} for {self.seat.seat_number} at {self.theater.name}'  
       
        
