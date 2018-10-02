from django.contrib import admin
from BracketApp import models

class ShowAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['show','subtitle']
    search_fields = ['show__name','subtitle']
    list_filter = ['show']
    list_display = ['show','subtitle']
    list_editable = ['subtitle']

class PlayerAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class ContestantAdmin(admin.ModelAdmin):
    fields = ['season','first_name','last_name','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    search_fields = ['season__name','first_name','last_name']
    list_filter = ['season']
    list_display = ['season','first_name','last_name','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    list_editable = ['first_name','last_name','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']

class BracketAdmin(admin.ModelAdmin):
    fields = ['season','player','contestant','predicted_elimination']
    search_fields = ['season__name','player__name','contestant']
    list_filter = ['season','player','predicted_elimination']
    list_display = ['season','player','contestant','predicted_elimination']
    list_editable = ['player','contestant','predicted_elimination']

class ScoreAdmin(admin.ModelAdmin):
    fields = ['player','elimination','rank','cum_score','points_back','score']
    search_fields = ['player','elimination']
    list_filter = ['player','elimination']
    list_display = ['player','elimination','rank','cum_score','points_back','score']

class BonusAdmin(admin.ModelAdmin):
    fields = ['season','player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    search_fields = ['season','player']
    list_filter = ['season','player']
    list_display = ['season','player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    list_editable = ['player','most_confessionals','most_individual_immunity_wins','most_votes_against']

# Register your models here.
admin.site.register(models.Show,ShowAdmin)
admin.site.register(models.Season,SeasonAdmin)
admin.site.register(models.Player,PlayerAdmin)
admin.site.register(models.Contestant,ContestantAdmin)
admin.site.register(models.Bracket,BracketAdmin)
admin.site.register(models.Score,ScoreAdmin)
admin.site.register(models.Bonus,BonusAdmin)
