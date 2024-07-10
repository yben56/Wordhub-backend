import numpy as np
import pandas as pd
from datetime import datetime, timezone

def recommend(data, weight, quiz=False, discount=0.9):
    df = pd.DataFrame(data)

    #1. days
    df = days(df)
    
    if quiz:
        #1. odd ratio
        df['odds'] = round(df['trials'] / df['correct'], 2)
        
        #2. cap (1. set cap prevent over weight, 2. if trials / 0 = cap)
        df['odds'] = df['odds'].clip(upper=5)

        #3. approach to 0 set odds <= '1.25' ex. 1/1, 5/4, 10/8, 100/98,
        df['odds'] = df['odds'].apply(lambda x: 0 if x <= 1.25 else x)

        #4. counts = odds ratio * weight * discount^t
        df['counts'] = df['odds'] * weight * np.power(discount, df['days'])
    else:
        #1. counts = weight * discount^t
        df['counts'] = weight * np.power(discount, df['days'])
    
    #2. group and sum
    df = df.groupby('word')['counts'].sum().reset_index()

    return df

def days(df):
    df['date'] = pd.to_datetime(df['date'])
    now = datetime.now(timezone.utc)
    df['days'] = df['date'].apply(lambda x: (now - x).days)

    return df