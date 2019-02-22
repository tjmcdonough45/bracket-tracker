import django
from django.db import models
# from django_pandas.managers import DataFrameManager
# from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,default=1,on_delete=models.PROTECT) #contains fields in default Django user model: username, e-mail, first_name, last_name, date_joined, last_login; permission-related fields: password, is_superuser, is_staff, is_active

    #additional fields
    profile_pic = models.ImageField(upload_to='BracketApp/profile_pics',blank=True)

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfileInfo.objects.create(user=instance)
    #     instance.profile.save()

    class Meta:
        verbose_name_plural = 'UserProfileInfo'

class Show(models.Model):
    name = models.CharField(max_length=69,default='Survivor')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Season(models.Model):
    show = models.ForeignKey(Show,default=1,on_delete=models.PROTECT)
    subtitle = models.CharField(max_length=69,default='David vs. Goliath')
    premiere = models.DateTimeField(default = django.utils.timezone.now)
    current_elimination = models.PositiveIntegerField(default=0)
    current_season = models.BooleanField(default=False)
    first_scored_elimination = models.PositiveIntegerField(default=1)
    season_pic = models.ImageField(upload_to='BracketApp/season_pics',blank=True)

    def __str__(self):
        return "%s: %s" % (self.show, self.subtitle)

    class Meta:
        ordering = ['show','-premiere']

class Point(models.Model):
    season = models.ForeignKey(Season,default=1,on_delete=models.PROTECT)
    rank = models.PositiveIntegerField(default=69)
    elimination = models.PositiveIntegerField(default=69)
    points_per_contestant_remaining = models.PositiveIntegerField(default=0)
    num_boots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s, %s, %s, %s" % (self.season, self.elimination, self.points_per_contestant_remaining, self.num_boots)

    class Meta:
        ordering = ['elimination']

class Player(models.Model):
    user = models.ForeignKey(UserProfileInfo,default=1,on_delete=models.PROTECT)
    season = models.ForeignKey(Season,default=1,on_delete=models.PROTECT)
    name = models.CharField(max_length=69,default='John Snow')
    # first_name = models.CharField(max_length=69,default='John')
    # last_name = models.CharField(max_length=69,default='Snow')

    def __str__(self):
        return "%s (%s, %s)" % (self.name,self.season,self.user)

    def get_absolute_url(self):
        return reverse('BracketApp:current_season')
        # return reverse('BracketApp:current_season',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['name']

class Contestant(models.Model):
    season = models.ForeignKey(Season,default=1,on_delete=models.PROTECT,related_name='contestants')
    first_name = models.CharField(max_length=69,default='John')
    last_name = models.CharField(max_length=69,default='Snow')
    shameful_exit = models.BooleanField(default=False)
    actual_rank = models.PositiveIntegerField(default=69)
    actual_elimination = models.PositiveIntegerField(default=69)
    num_confessionals = models.PositiveIntegerField(default=0)
    num_individual_immunity_wins = models.PositiveIntegerField(default=0)
    num_votes_against = models.PositiveIntegerField(default=0)

    def __str__(self):
        # return "%s %s (%s)" % (self.first_name, self.last_name, self.season)
        return "%s %s" % (self.first_name, self.last_name)

#     objects = DataFrameManager()

    class Meta:
        ordering = ['season','actual_rank']

class Bracket(models.Model):
    player = models.ForeignKey(Player,default=1,on_delete=models.PROTECT)
    contestant = models.ForeignKey(Contestant,default=1,on_delete=models.PROTECT)
    predicted_rank = models.PositiveIntegerField(default=0)
    predicted_elimination = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s, %s, %s" % (self.player, self.contestant, self.predicted_elimination)

#     objects = DataFrameManager()

    class Meta:
        ordering = ['player','predicted_rank']

class Score(models.Model):
    player = models.ForeignKey(Player,default=1,on_delete=models.PROTECT)
    elimination = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    cum_score = models.IntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    points_back = models.PositiveIntegerField(default=0)
    maximum_points_remaining = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s, %s, %s" % (self.player, self.elimination, self.cum_score)

    class Meta:
        ordering = ['player','elimination']

class Bonus(models.Model):
    player = models.ForeignKey(Player, default=1,on_delete=models.PROTECT)
    most_confessionals = models.ForeignKey(Contestant, default=1, related_name='q1', on_delete=models.PROTECT)
    most_individual_immunity_wins = models.ForeignKey(Contestant, default=1, related_name='q2', on_delete=models.PROTECT)
    most_votes_against = models.ForeignKey(Contestant, default=1, related_name='q3', on_delete=models.PROTECT)

    def __str__(self):
        return "%s, c: %s, ii: %s, va: %s" % (self.player, self.most_confessionals,self.most_individual_immunity_wins,self.most_votes_against)

    class Meta:
        ordering = ['player']
        verbose_name_plural = 'Bonuses'
