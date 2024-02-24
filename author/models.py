from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver

from . validators import validate_possible_number
from phonenumber_field.modelfields import PhoneNumberField
from. helper import get_last_pk,delete_files
# Create your models here.


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""
    default_validators = [validate_possible_number]


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=200,unique=True)


def author_image(instance, filename):
    instance_id = get_last_pk(instance)
    ext = filename.split(".")[-1]
    newname = "author/" + str( instance_id + 1) + "." + ext
    return newname  


class Author(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    rating = models.PositiveBigIntegerField(default=0)
    phone = PossiblePhoneNumberField(unique=True)
    image = models.FileField(upload_to=author_image)

    @property
    def name(self):
        return '{0} {1}'.format(self.first_name,self.last_name)

@receiver(signal=post_delete,sender=Author)
def delete_user_documentattachment(sender,instance,*args,**kwargs):
    if instance.image:
        delete_files(instance.image.path)
    
class AuthorBook(models.Model):
   created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
   author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author')
   book  = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='author_book')
   is_active  = models.BooleanField(default=True)

   class Meta:
       unique_together = ('author','book')

class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    name = models.CharField(max_length=50)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author_review',null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_review',null=True,blank=True)
    review = models.TextField()

