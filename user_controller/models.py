from django.contrib.auth.base_user import BaseUserManager
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from django.core.cache import cache 
import datetime
from django.conf import settings


class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, password, **extra_fields):
       
        if not username:
            raise ValueError(_('The Username must not be left blank.'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(_("email address"), unique=True)
    
    is_active = models.BooleanField(_("Is active"), default=False)
    is_staff = models.BooleanField(_("Staff?"), default=False)
    is_superuser = models.BooleanField(_("Superuser?"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id} - {self.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="user_profiles", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    friends = models.ManyToManyField(CustomUser, related_name="user_friends", through="Friends")
    is_online = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.user.username}"

    class Meta:
        ordering = ("-created_at",)


class Friends(models.Model):
    profile = models.ForeignKey(UserProfile, related_name="from_friend", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="to_friend", on_delete=models.CASCADE)
    
    @classmethod
    def can_add_friend(cls, user):
        if cls.objects.filter(user=user).exists():
            return False
        return True
        
    def __str__(self):
        return f" {self.id} - {self.user.username}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name="from_user", on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.ForeignKey(CustomUser, related_name="to_user", on_delete=models.CASCADE, null=True, blank=True)
    accepted = models.BooleanField(default=False)

    @classmethod
    def can_send_request(cls, user):
        if cls.objects.filter(to_user=user).exists():
            return False
        return True
    
    def accept(self):
        user = get_object_or_404(CustomUser, username=self.from_user.username)
        user2 = get_object_or_404(CustomUser, username=self.to_user.username)
        try:
            #create friend instance for request sender with the request acceptor
            Friends.objects.create(profile=user.user_profiles, user=self.to_user)
            #create friend instance for request acceptor with request sender
            Friends.objects.create(profile=user2.user_profiles, user=self.from_user)
        except IntegrityError:
            pass
    
        self.accepted = True
        self.save()

    def reject(self):
        self.accepted = False
        self.save()

    def __str__(self):
        return f"{self.from_user.username} sent friend request to {self.to_user.username}"