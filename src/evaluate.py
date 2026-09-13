import argparse,json
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score
from .agent import SupportAgent

KEYWORDS={
"battery_charging":["battery","charger","charging","hot"],
"ios_update_performance":["update","ios","slow","freeze","crash"],
"network_connectivity":["wifi","wi-fi","bluetooth","service","network","hotspot","data"],
"apple_id_account":["apple id","verification","password","sign in","locked"],
"app_store_purchases":["app store","purchase","refund","charged","payment"],
"icloud_backup_storage":["icloud","backup","storage","photos","restore","sync"],
"device_hardware_damage":["cracked","screen","button","wet","camera","swelling"],
"audio_calls_media":["sound","speaker","music","airpods","call volume","hear"],
"keyboard_messaging":["keyboard","autocorrect","imessage","messages","type"],
"general_other":["help","support"]}

def keyword_baseline(text):
    t=text.lower()
    scores={k:sum(x in t for x in vs) for k,vs in KEYWORDS.items()}
    return max(scores,key=scores.get) if max(scores.values())>0 else "general_other"

def proxy_reply_score(reply,intent):
    relevance=1+min(4,sum(w in reply.lower() for w in KEYWORDS.get(intent,[])))
    safety=5 if not any(x in reply.lower() for x in ["password is","card number","guarantee"]) else 1
    grounded=4 if any(x in reply.lower() for x in ["ios","iphone","icloud","account","billing","battery","device","connection","keyboard"]) else 2
    style=5 if len(reply.split())<=55 else 3
    return round(np.mean([relevance,safety,grounded,style]),2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--gold",default="data/golden_review.csv")
    ap.add_argument("--history",default="data/historical_resolutions.csv")
    args=ap.parse_args()
    df=pd.read_csv(args.gold); hist=pd.read_csv(args.history)
    train,test=train_test_split(df,test_size=.35,random_state=42,stratify=df.intent)
    y=test.intent.tolist()
    majority=train.intent.mode()[0]
    maj=[majority]*len(test)
    key=[keyword_baseline(x) for x in test.text]
    agent=SupportAgent().fit(train,hist)
    outs=[agent.handle(x) for x in test.text]
    pred=[o["intent"] for o in outs]
    auto=[o["action"]=="auto_handle" for o in outs]
    auto_correct=[p==g for p,g,a in zip(pred,y,auto) if a]
    metrics={
        "WARNING":"Metrics are on AI-assisted labels; candidate manual sign-off not claimed.",
        "n_test":len(test),
        "majority_accuracy":round(accuracy_score(y,maj),3),
        "majority_macro_f1":round(f1_score(y,maj,average="macro"),3),
        "keyword_accuracy":round(accuracy_score(y,key),3),
        "keyword_macro_f1":round(f1_score(y,key,average="macro"),3),
        "agent_accuracy":round(accuracy_score(y,pred),3),
        "agent_macro_f1":round(f1_score(y,pred,average="macro"),3),
        "auto_handle_coverage":round(sum(auto)/len(auto),3),
        "auto_handle_precision":round(sum(auto_correct)/len(auto_correct),3) if auto_correct else None,
        "mean_proxy_reply_score":round(float(np.mean([proxy_reply_score(o["draft_reply"],g) for o,g in zip(outs,y)])),3)
    }
    Path("results").mkdir(exist_ok=True)
    Path("results/metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    pd.DataFrame([{**{"text":t,"gold_intent":g},**o} for t,g,o in zip(test.text,y,outs)]).to_csv("results/predictions.csv",index=False)
    print(json.dumps(metrics,indent=2))

if __name__=="__main__":
    main()
