# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','BracketHub.settings')
#
# import django
# django.setup()

from django.core.management.base import BaseCommand
from BracketApp.models import Season,Player,Contestant,Bracket,Score,Bonus
from django_pandas.io import read_frame
import numpy as np
import pandas as pd
# from sqlalchemy import create_engine
# from django.db import transaction

def score():
    qs_season = Season.objects.filter(current_season__exact=True).values()[0]
    cur_elimination = qs_season['current_elimination']
    first_scored_elimination = qs_season['first_scored_elimination']

    qs_bracket = Bracket.objects.filter(season__current_season__exact=True)
    df_bracket = read_frame(qs_bracket)
    # print(df_bracket.head(),'\n')

    qs_contestant = Contestant.objects.filter(season__current_season__exact=True)
    # print(len(qs_contestant.values_list('last_name',flat=True)))
    df_contestant = read_frame(qs_contestant)
    df_contestant['contestant'] = df_contestant['first_name'] + ' ' + df_contestant['last_name']
    df_contestant.drop(columns=['first_name','last_name'],inplace=True)
    # print(df_contestant.head(),'\n')
    num_eliminations = len(df_contestant['contestant'].unique())-1

    players=df_bracket['player'].unique()
    stats = ['score','cum_score','rank','points_back']
    columns = pd.MultiIndex.from_product([np.arange(first_scored_elimination,cur_elimination+1), stats])
    df_score = pd.DataFrame(np.zeros((len(players),(cur_elimination-first_scored_elimination+1)*len(stats)),dtype=int),index=players,columns=columns)

    for label,df in df_bracket.groupby('player'):
        df2 = df.merge(df_contestant,how='outer',on='contestant')

        #identify winner picks and determine if any of said picks had shameful exits
        winners = df2[df2['predicted_rank']==1]
        if winners['shameful_exit'].values[0]:
            shame = winners['actual_elimination'].values[0]
        else:
            shame = 0

        #score N points per player correctly guessed to survive Nth scoring elimination
        df3 = df2[df2['actual_elimination']<=first_scored_elimination]
        df2['num_eliminations_survived'] = df2[['predicted_elimination','actual_elimination']].min(axis=1)-1
        for i in np.arange(first_scored_elimination,cur_elimination+1):
            test = (df2['num_eliminations_survived']>=i)*(i-first_scored_elimination+1)
            if i == shame:
                df_score.loc[label,(i,'score')] = test.sum()-30 #30 point deduction for a winner pick having a shameful exit in the given elimination
            else:
                df_score.loc[label,(i,'score')] = test.sum()

    #score 40 bonus points per correct answer to bonus questions
    if cur_elimination==num_eliminations:
        qs_bonus = Bonus.objects.filter(season__current_season__exact=True)
        df_bonus = read_frame(qs_bonus)
        # print(df_bonus.head())
        df_contestant.set_index('contestant',inplace=True)
        test=df_contestant[['num_confessionals','num_individual_immunity_wins','num_votes_against']].idxmax()
        # print(test.values)

        categories=['most_confessionals','most_individual_immunity_wins','most_votes_against']
        i=0
        for cat in categories:
            b = df_bonus[df_bonus[cat]==test.values[i]]['player'].values
            df_score.loc[b,(cur_elimination,'score')] = df_score.loc[b,(cur_elimination,'score')]+40
            i=i+1

    idx = pd.IndexSlice

    test = df_score.loc[:, idx[:, 'score']].cumsum(axis=1)
    test2 = test.rank(axis=0,method='dense',ascending=False)
    test3 = test.max(axis=0)-test

    test.rename(columns={'score':'cum_score'},inplace=True)
    test2.rename(columns={'score':'rank'},inplace=True)
    test3.rename(columns={'score':'points_back'},inplace=True)

    df_score.loc[:, idx[:, 'cum_score']] = test
    df_score.loc[:, idx[:, 'rank']] = test2
    df_score.loc[:, idx[:, 'points_back']] = test3

    # print(df_score,'\n')

    df_score = df_score.stack(level=0).reset_index().rename(index=str,columns={'level_0':'player','level_1':'elimination'})

    # engine = create_engine('sqlite:///db.sqlite3',echo=False)
    # df_score.to_sql(name=Score,con=engine,if_exists='replace',index=False)

    Score.objects.all().delete()

    dict_score = df_score.to_dict('records')
    # print(dict_score,'\n')
    s = Season.objects.get(current_season=True)
    for dict in dict_score:
        p = Player.objects.get(name=dict['player'])
        Score.objects.update_or_create(season=s,player=p,elimination=dict['elimination'],score=dict['score'],cum_score=dict['cum_score'],rank=dict['rank'],points_back=dict['points_back'])
    # Score.objects.bulk_create(Score(**vals) for vals in dict_score)

    # @transaction.commit_manually
    # def save(df):
    #     for item in df.to_dict('records'):
    #         entry = Score(**item)
    #         entry.save()
    #     transaction.commit()
    # save(df_score)

    if __name__ == '__main__':
        print('Score')
        print(df_score)

class Command(BaseCommand):

    #Show this when the user types help
    help="Score brackets"

    #A command must define handle()
    def handle(self,**options):
        score()
        self.stdout.write('Scoring brackets.')
