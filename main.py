import pandas as pd


df=pd.read_csv('dataset.csv')

# 1. 
# a)Total number of matches
print(len(df))

#b)Column names
print((df.columns).to_list())

#c)First 5 rows of data
print(df.head())

#d)Describe the data
print(df.describe())


#2.Which player has won the most “Player of the Match” awards in games decided on the final ball? (i.e., matches won by just 1 run or 1 wicket)
matches=df[((df['win_by_runs']==1)|(df['win_by_wickets']==1))]
res=matches['player_of_match'].value_counts().idxmax()
print(res)

#3.At Wankhede Stadium,is it more common to win by batting first(runs)or by batting second(wickets)?
matches=df[(df["venue"]=="Wankhede Stadium")]
batting_first=(matches["win_by_runs"]>0).sum()
batting_second=(matches["win_by_wickets"]>0).sum()
if batting_first>batting_second:
    print("Common to win by batting first")
else:
    print("Common to win by batting second")

#4.Which team has the highest number of wins where the victory margin was greater than 50 runs?
greater_than_50=df[df["win_by_runs"]>50]
res=greater_than_50.groupby("winner")
print(res["winner"].value_counts().idxmax())

#5.How many times has the team that won the toss also set a target and won the match?
res=df[(df["toss_winner"]==df["winner"])]
print(len(res))

#6.Which of the two umpires (umpire1 or umpire2) has officiated more matches involving the Kolkata Knight Riders?
kkr_matches=df[(df["team1"]=="Kolkata Knight Riders") | (df["team2"]=="Kolkata Knight Riders")]
umpire1_count=kkr_matches["umpire1"].value_counts().idxmax()
umpire2_count=kkr_matches["umpire2"].value_counts().idxmax()
if umpire1_count>umpire2_count:
    print("Umpire 1 has officiated more matches")
else:
    print("Umpire 2 has officiated more matches")
