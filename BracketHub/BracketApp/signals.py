from BracketApp.models import Season,Score
from django.db.models.signals import post_save
from django.dispatch import receiver
from BracketApp.management.commands.score import score

@receiver(post_save,sender=Season)
def run_score(sender,instance,created,**kwargs):
    if not created:
        num_eliminations = instance.current_elimination
        score(num_eliminations)
    return(num_eliminations)
