"""Extract AppleSupport inbound requests and directly-linked replies from Kaggle twcs.csv."""
import argparse,pandas as pd
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument("--input",default="data/raw/twcs.csv")
ap.add_argument("--out",default="data/apple_pairs.csv")
ap.add_argument("--max",type=int,default=12000)
a=ap.parse_args()

df=pd.read_csv(a.input,dtype=str).fillna("")
df["inbound"]=df["inbound"].str.lower().eq("true")
by_id=df.set_index("tweet_id")
rows=[]
for _,r in df[df.inbound].iterrows():
    ids=[x.strip() for x in r.response_tweet_id.split(",") if x.strip()]
    for rid in ids:
        if rid in by_id.index:
            rr=by_id.loc[rid]
            if isinstance(rr,pd.DataFrame): rr=rr.iloc[0]
            if rr.author_id=="AppleSupport":
                rows.append({"tweet_id":r.tweet_id,"created_at":r.created_at,"text":r.text,"historical_reply":rr.text})
                break
    if len(rows)>=a.max: break
Path(a.out).parent.mkdir(parents=True,exist_ok=True)
pd.DataFrame(rows).to_csv(a.out,index=False)
print(f"wrote {len(rows)} AppleSupport request/reply pairs")
