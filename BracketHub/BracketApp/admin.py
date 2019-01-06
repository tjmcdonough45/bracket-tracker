from django.contrib import admin
from BracketApp.models import UserProfileInfo,Show,Season,Player,Contestant,Bracket,Score,Bonus,UserProfileInfo

class UserProfileInfoAdmin(admin.ModelAdmin):
    fields = ['user','profile_pic']
    list_display = ['user','profile_pic','players']

    def players(self,obj):
         return ", ".join([player.name for player in obj.player_set.all()])

class ShowAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['show','subtitle','premiere','current_season','first_scored_elimination','current_elimination']
    search_fields = ['show__name','subtitle']
    list_filter = ['show']
    list_display = ['show','subtitle','premiere','current_season','first_scored_elimination','current_elimination','players']
    list_editable = ['current_season','current_elimination']

    def players(self,obj):
         return ", ".join([player.name for player in obj.player_set.all()])

class PlayerAdmin(admin.ModelAdmin):
    fields = ['user','season','name']
    search_fields = ['name']
    list_filter = ['season']
    list_display = ['user','name','season']
    # list_editable = ['name']

class ContestantAdmin(admin.ModelAdmin):
    fields = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    search_fields = ['season__name','first_name','last_name']
    list_filter = ['season']
    list_display = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    list_editable = ['actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']

class BracketAdmin(admin.ModelAdmin):
    fields = ['player','contestant','predicted_rank','predicted_elimination']
    search_fields = ['player__name','contestant']
    list_filter = ['player','predicted_rank']
    list_display = ['player','contestant','predicted_rank','predicted_elimination']
    list_editable = ['contestant','predicted_rank']

class ScoreAdmin(admin.ModelAdmin):
    fields = ['player','elimination','rank','cum_score','points_back','score','maximum_points_remaining']
    search_fields = ['player__name','elimination']
    list_filter = ['player','elimination']
    list_display = ['player','elimination','rank','cum_score','points_back','score','maximum_points_remaining']

class BonusAdmin(admin.ModelAdmin):
    fields = ['player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    search_fields = ['player']
    list_filter = ['player']
    list_display = ['player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    list_editable = ['most_confessionals','most_individual_immunity_wins','most_votes_against']

# Register your models here.
admin.site.register(UserProfileInfo,UserProfileInfoAdmin)
admin.site.register(Show,ShowAdmin)
admin.site.register(Season,SeasonAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(Contestant,ContestantAdmin)
admin.site.register(Bracket,BracketAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Bonus,BonusAdmin)
