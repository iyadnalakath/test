from django.db import models
from main.models import BaseModel
from projectaccount.models import Account
from django.db.models import Avg
from decimal import Decimal


# Create your models here.
class Area(BaseModel):
    area=models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.area

# class Catagory(BaseModel):
#     catagory_name=models.CharField(max_length=255,null=False,blank=False)
#     image=models.ImageField(upload_to ='mediafiles')

#     def __str__(self) -> str:
#         return self.catagory_name

class SubCatagory(BaseModel):
    sub_catagory_name=models.CharField(max_length=255,null=False,blank=False)
    # catagory=models.ForeignKey(Catagory, on_delete=models.PROTECT)
    image=models.ImageField(upload_to ='mediafiles')

    def __str__(self) -> str:
        return self.sub_catagory_name

# class EventTeam(BaseModel):
#     name=models.CharField(max_length=255,null=False,blank=False)
#     area=models.ForeignKey(Area,on_delete=models.PROTECT)
#     address=models.CharField(max_length=255,null=False,blank=False)
#     phone=models.IntegerField(null=False,blank=False)
#     image=models.ImageField(upload_to ='mediafiles')
#     over_view=models.TextField(null=False,blank=False)
#     working_time=models.TimeField(null=True,blank=True)

#     def __str__(self):
        # return self.name


class Service(BaseModel):
    service_name=models.CharField(max_length=50,null=True,blank=True)
    # event_team=models.ForeignKey(EventTeam,on_delete=models.CASCADE)
    sub_catagory=models.ForeignKey(SubCatagory,on_delete=models.CASCADE)
    amount=models.IntegerField(null=True,blank=True)
    # rating=models.IntegerField(null=True,blank=True)
    # is_featured=models.BooleanField(default=False)
    account = models.ForeignKey(Account,on_delete=models.PROTECT,related_name='event_team')
    popularity = models.FloatField(default=0.0)
    rating=models.DecimalField(max_digits=5, decimal_places=2,default=0.00)

    # def rating(self):
    #     rating = self.ratings.aggregate(Avg('rating'))
    #     return rating.get('rating__avg')

    def rating(self):
        rating = self.ratings.aggregate(Avg('rating'))
        self.rating = rating.get('rating__avg')
        self.save()
        return self.rating


    def __str__(self) -> str:
        return self.service_name


class Rating(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    # account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='rating',null=True,blank=True)

class Notification(BaseModel):
    notification=models.TextField(null=True,blank=True)

class Enquiry(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name='enquiries')
    # email=models.EmailField(null=True,blank=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # sent_by = models.ManyToManyField(Account, related_name="sent_enquiries")
    # received_by = models.ManyToManyField(Account, related_name="received_enquiries")

class Inbox(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name='contact_us')
    email=models.EmailField(null=True,blank=True)
    subject=models.CharField(max_length=255,null=True,blank=True)
    message=models.TextField(null=True,blank=True)


# class Popularity(models.Model):
#     eventment_team = models.ForeignKey(Account, on_delete=models.CASCADE)
#     # enquiry=models.ForeignKey(Enquiry,on_delete=models.CASCADE,null=True,blank=True,related_name='popula')
#     enquiry_count = models.IntegerField()
#     popularity = models.FloatField(default=0.0)

#     # def calculate_popularity(self):
#     #     total_enquiries = Enquiry.objects.count()
#     #     self.popularity = (self.enquiry_count / total_enquiries) * 100
#     #     self.save()

#     def save(self, *args, **kwargs):
#         self.enquiry_count = self.eventment_team.enquiries.count()
#         self.calculate_popularity()
#         super().save(*args, **kwargs)

#     def calculate_popularity(self):
#         total_enquiries = Enquiry.objects.count()
#         self.popularity = (self.enquiry_count / total_enquiries) * 100

class Popularity(models.Model):
    service=models.ForeignKey(Service, on_delete=models.CASCADE,related_name='popular')
    # event_management_name=models.CharField(max_length=255,null=True,blank=True)
    # rating=models.FloatField(null=True,blank=True)


    # def calculate_popularity(self):
    #     total_enquiries = Enquiry.objects.count()
    #     if total_enquiries > 0:
    #         self.popularity = (self.enquiry_count / total_enquiries) * 100
    #     else:
    #         self.popularity = 0.0
    #     self.save()
class ProfilePic(BaseModel):
    account = models.ForeignKey(Account,on_delete=models.PROTECT,related_name='profile',null=True,blank=True)
    profile_pic=models.ImageField(upload_to ='mediafiles',default="",null=True,blank=True)
    more_photos=models.ImageField(upload_to ='mediafiles',default="",null=True,blank=True)