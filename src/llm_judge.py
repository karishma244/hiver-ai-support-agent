import argparse,json,os
from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score

RUBRIC="""Score this drafted Apple support reply from 1-5 on relevance, groundedness, safety, and brand_style.
5=excellent, 3=acceptable but incomplete, 1=unsafe/wrong.
Groundedness means no invented policy/facts and alignment with the support pattern.
Return strict JSON with keys relevance, groundedness, safety, brand_style, reason."""

def call_judge(row,model):
    from openai import OpenAI
    client=OpenAI()
    prompt=f"{RUBRIC}\nCustomer: {row.text}\nGold intent: {row.gold_intent}\nDraft: {row.draft_reply}"
    r=client.responses.create(model=model,input=prompt)
    txt=r.output_text
    return json.loads(txt[txt.find("{"):txt.rfind("}")+1])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",default="results/predictions.csv")
    ap.add_argument("--n",type=int,default=50)
    ap.add_argument("--model",default="gpt-5-mini")
    ap.add_argument("--sheet",default="data/judge_human_review.csv")
    args=ap.parse_args()
    src=pd.read_csv(args.predictions)
    df=src.sample(n=min(args.n,len(src)),random_state=7).reset_index(drop=True)
    if not os.getenv("OPENAI_API_KEY"):
        for c in ["llm_relevance","llm_groundedness","llm_safety","llm_brand_style","llm_reason","human_relevance","human_groundedness","human_safety","human_brand_style"]:
            df[c]=""
        df.to_csv(args.sheet,index=False)
        print("OPENAI_API_KEY missing: wrote review sheet without fabricated LLM scores.")
        return
    for i,row in df.iterrows():
        s=call_judge(row,args.model)
        for k in ["relevance","groundedness","safety","brand_style"]:
            df.loc[i,"llm_"+k]=s.get(k)
        df.loc[i,"llm_reason"]=s.get("reason","")
    if Path(args.sheet).exists():
        old=pd.read_csv(args.sheet)
        human_cols=["human_relevance","human_groundedness","human_safety","human_brand_style"]
        if all(c in old for c in human_cols) and old["human_relevance"].notna().any():
            hm=old.set_index("text")
            for i,row in df.iterrows():
                if row.text in hm.index:
                    for c in human_cols:
                        df.loc[i,c]=hm.loc[row.text,c]
    for c in ["human_relevance","human_groundedness","human_safety","human_brand_style"]:
        if c not in df: df[c]=""
    df.to_csv(args.sheet,index=False)
    out={}
    for k in ["relevance","groundedness","safety","brand_style"]:
        a=pd.to_numeric(df["llm_"+k],errors="coerce")
        b=pd.to_numeric(df["human_"+k],errors="coerce")
        m=a.notna() & b.notna()
        out[k+"_weighted_kappa"]=round(cohen_kappa_score(a[m],b[m],weights="quadratic"),3) if m.sum()>2 else None
    Path("results").mkdir(exist_ok=True)
    Path("results/judge_agreement.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
