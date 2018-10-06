from django.contrib import admin
from BracketApp.models import Show,Season,Player,Contestant,Bracket,Score,Bonus

class ShowAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class SeasonAdmin(admin.ModelAdmin):
    fields = ['show','subtitle','current_season','first_scored_elimination','current_elimination']
    search_fields = ['show__name','subtitle']
    list_filter = ['show']
    list_display = ['show','subtitle','current_season','first_scored_elimination','current_elimination']
    list_editable = ['current_season','current_elimination']

class PlayerAdmin(admin.ModelAdmin):
    fields = ['name']
    # search_fields = ['name']
    # list_filter = ['name']
    # list_display = ['name']
    # list_editable = ['name']

class ContestantAdmin(admin.ModelAdmin):
    fields = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    search_fields = ['season__name','first_name','last_name']
    list_filter = ['season']
    list_display = ['season','first_name','last_name','actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']
    list_editable = ['actual_rank','actual_elimination','num_confessionals','num_individual_immunity_wins','num_votes_against','shameful_exit']

class BracketAdmin(admin.ModelAdmin):
    fields = ['season','player','contestant','predicted_rank','predicted_elimination']
    search_fields = ['season__name','player__name','contestant']
    list_filter = ['season','player','predicted_rank','predicted_elimination']
    list_display = ['season','player','contestant','predicted_rank','predicted_elimination']
    list_editable = ['contestant','predicted_rank','predicted_elimination']

class ScoreAdmin(admin.ModelAdmin):
    fields = ['season','player','elimination','rank','cum_score','points_back','score']
    search_fields = ['season__name','player__name','elimination']
    list_filter = ['season','player','elimination']
    list_display = ['season','player','elimination','rank','cum_score','points_back','score']

class BonusAdmin(admin.ModelAdmin):
    fields = ['season','player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    search_fields = ['season','player']
    list_filter = ['season','player']
    list_display = ['season','player','most_confessionals','most_individual_immunity_wins','most_votes_against']
    list_editable = ['most_confessionals','most_individual_immunity_wins','most_votes_against']

# Register your models here.
admin.site.register(Show,ShowAdmin)
admin.site.register(Season,SeasonAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(Contestant,ContestantAdmin)
admin.site.register(Bracket,BracketAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Bonus,BonusAdmin)
