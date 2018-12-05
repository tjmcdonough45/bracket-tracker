import django
from django.db import models
# from django_pandas.managers import DataFrameManager
# from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT) #contains fields in default Django user model: username, e-mail, first_name, last_name, date_joined, last_login; permission-related fields: password, is_superuser, is_staff, is_active

    #additional fields
    profile_pic = models.ImageField(upload_to='BracketApp/profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Show(models.Model):
    name = models.CharField(max_length=69,default='Survivor')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Season(models.Model):
    show = models.ForeignKey(Show, default=69, on_delete=models.PROTECT)
    subtitle = models.CharField(max_length=69,default='David vs. Goliath')
    premiere = models.DateField(default = django.utils.timezone.now)
    current_elimination = models.PositiveIntegerField(default=0)
    current_season = models.BooleanField(default=False)
    first_scored_elimination = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s: %s" % (self.show, self.subtitle)

    class Meta:
        ordering = ['show','-premiere']

class Player(models.Model):
    name = models.CharField(max_length=69,default='John Snow')
    season = models.ManyToManyField(Season)
    # first_name = models.CharField(max_length=69,default='John')
    # last_name = models.CharField(max_length=69,default='Snow')

    def __str__(self):
        return self.name
        # return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('BracketApp:current_season')
        # return reverse('BracketApp:current_season',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['name']

class Contestant(models.Model):
    season = models.ForeignKey(Season,on_delete=models.PROTECT,related_name='contestants')
    first_name = models.CharField(max_length=69,default='John')
    last_name = models.CharField(max_length=69,default='Snow')
    shameful_exit = models.BooleanField(default=False)
    actual_rank = models.PositiveIntegerField(default=69)
    actual_elimination = models.PositiveIntegerField(default=69)
    num_confessionals = models.PositiveIntegerField(default=0)
    num_individual_immunity_wins = models.PositiveIntegerField(default=0)
    num_votes_against = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

#     objects = DataFrameManager()

    class Meta:
        ordering = ['season','actual_rank']

class Bracket(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    contestant = models.ForeignKey(Contestant, on_delete=models.PROTECT)
    predicted_rank = models.PositiveIntegerField(default=0)
    predicted_elimination = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s, %s, %s" % (self.player, self.contestant, self.predicted_elimination)

#     objects = DataFrameManager()

    class Meta:
        ordering = ['season','player','predicted_rank']

class Score(models.Model):
    season = models.ForeignKey(Season, default=69, on_delete=models.PROTECT)
    player = models.ForeignKey(Player,on_delete=models.PROTECT)
    elimination = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    cum_score = models.IntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    points_back = models.PositiveIntegerField(default=0)
    maximum_points_remaining = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s" % (self.player)

    class Meta:
        ordering = ['season','player','elimination']

class Bonus(models.Model):
    season = models.ForeignKey(Season, default=69, on_delete=models.PROTECT)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    most_confessionals = models.ForeignKey(Contestant, related_name='q1', on_delete=models.PROTECT)
    most_individual_immunity_wins = models.ForeignKey(Contestant, related_name='q2', on_delete=models.PROTECT)
    most_votes_against = models.ForeignKey(Contestant, related_name='q3', on_delete=models.PROTECT)

    def __str__(self):
        return "%s, %s" % (self.season,self.player)

    class Meta:
        ordering = ['season','player']
        verbose_name_plural = 'Bonuses'
