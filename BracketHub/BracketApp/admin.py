from django.contrib import admin
from BracketApp.models import UserProfileInfo,Show,Season,Point,Player,Contestant,Bracket,Score,Bonus,UserProfileInfo

class UserProfileInfoAdmin(admin.ModelAdmin):
    fields = ['user','profile_pic']
    list_display = ['user','profile_pic','seasons','players']

    def players(self,obj):
         return ", ".join([player.name for player in obj.player_set.all().order_by('-season__premiere')])

    def seasons(self,obj):
        return ", ".join([player.season.subtitle for player in obj.player_set.all().order_by('-season__premiere')])

class ShowAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['show','subtitle','premiere','current_season','first_scored_elimination','current_elimination','season_pic']
    search_fields = ['show__name','subtitle','users']
    list_filter = ['show']
    list_display = ['show','subtitle','premiere','current_season','first_scored_elimination','current_elimination','season_pic','users','players']
    list_editable = ['current_season','current_elimination']

    def players(self,obj):
         return ", ".join([player.name for player in obj.player_set.all()])

    def users(self,obj):
        return ", ".join([player.user.user.username for player in obj.player_set.all()])

class PointAdmin(admin.ModelAdmin):
    fields = ['season','rank','elimination','points_per_contestant_remaining','num_boots']
    list_filter = ['season']
    list_display = ['season','rank','elimination','points_per_contestant_remaining','num_boots']
    list_editable = ['rank','elimination','points_per_contestant_remaining','num_boots']

class PlayerAdmin(admin.ModelAdmin):
    fields = ['user','season','name']
    search_fields = ['user__user__username','name']
    list_filter = ['season']
    list_display = ['user','name','season']
    # list_editable = ['name']

class ContestantAdmin(admin.ModelAdmin):
    fields = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit','contestant_pic']
    search_fields = ['season__show__name','season__subtitle','first_name','last_name']
    list_filter = ['season']
    list_display = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    list_editable = ['actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']

class BracketAdmin(admin.ModelAdmin):
    fields = ['player','contestant','predicted_rank','predicted_elimination','submitted']
    search_fields = ['player__name','player__user__user__username','contestant__first_name','contestant__last_name']
    list_filter = ['player__season','player__user__user__username','predicted_rank']
    list_display = ['player','contestant','predicted_rank','predicted_elimination','submitted']
    list_editable = ['predicted_rank','predicted_elimination']

class ScoreAdmin(admin.ModelAdmin):
    fields = ['player','elimination','rank','cum_score','points_back','score','maximum_points_remaining']
    search_fields = ['player__name','player__user__user__username']
    list_filter = ['player__season','player__user__user__username','elimination']
    list_display = ['player','elimination','rank','cum_score','points_back','score','maximum_points_remaining']

class BonusAdmin(admin.ModelAdmin):
    fields = ['player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    search_fields = ['player__name','player__user__user__username']
    list_filter = ['player__season','player__user__user__username']
    list_display = ['player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    # list_editable = ['most_confessionals','most_individual_immunity_wins','most_votes_against']

# Register your models here.
admin.site.register(UserProfileInfo,UserProfileInfoAdmin)
admin.site.register(Show,ShowAdmin)
admin.site.register(Season,SeasonAdmin)
admin.site.register(Point,PointAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(Contestant,ContestantAdmin)
admin.site.register(Bracket,BracketAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Bonus,BonusAdmin)
