import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','BracketHub.settings')

import django
django.setup()

from BracketApp.models import Player,Contestant,Bracket,Score
from django_pandas.io import read_frame
import numpy as np
import pandas as pd
# from sqlalchemy import create_engine
# from django.db import transaction

qs_bracket = Bracket.objects.all()
df_bracket = read_frame(qs_bracket,fieldnames=['player','contestant','predicted_elimination'])

qs_contestant = Contestant.objects.all()
df_contestant = read_frame(qs_contestant,fieldnames=['first_name','last_name','shameful_exit','actual_elimination'])
df_contestant['contestant'] = df_contestant['first_name'] + ' ' + df_contestant['last_name']
df_contestant.drop(columns=['first_name','last_name'],inplace=True)

players=df_bracket['player'].unique()
# winners=df_bracket[]
num_eliminations = 4
stats = ['score','cum_score','rank','points_back']
columns = pd.MultiIndex.from_product([np.arange(num_eliminations)+1, stats])
df_score = pd.DataFrame(np.zeros((len(players),num_eliminations*len(stats)),dtype=int),index=players,columns=columns)

for label,df in df_bracket.groupby('player'):
    df2 = df.merge(df_contestant,how='outer',on='contestant')
    df2['num_eliminations_survived'] = df2[['predicted_elimination','actual_elimination']].min(axis=1)-1
    for i in np.arange(num_eliminations)+1:
        test = (df2['num_eliminations_survived']>=i)*i
        # test2 = (df2['shameful_exit']==i)*-30
        df_score.loc[label,(i,'score')] = test.sum()
        # df_score.loc[label,(i,'score')] = test.sum()+test2.sum()

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

df_score = df_score.stack(level=0).reset_index().rename(index=str,columns={'level_0':'player','level_1':'elimination'})

# engine = create_engine('sqlite:///db.sqlite3',echo=False)
# df_score.to_sql(name=Score,con=engine,if_exists='replace',index=False)

dict_score = df_score.to_dict('records')
Score.objects.bulk_create(
    Score(**vals) for vals in dict_score
)

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
