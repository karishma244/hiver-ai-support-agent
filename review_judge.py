import streamlit as st
import pandas as pd
from pathlib import Path

PATH=Path("data/judge_human_review.csv")
df=pd.read_csv(PATH)
dims=["relevance","groundedness","safety","brand_style"]

st.set_page_config(page_title="Judge Validation", layout="wide")
st.title("LLM judge vs human validation")
idx=st.number_input("Example", 1, len(df), 1)-1
r=df.iloc[idx]
st.progress((idx+1)/len(df))
st.subheader("Customer")
st.write(r["text"])
st.subheader("Draft")
st.write(r["draft_reply"])
vals={}
for d in dims:
    old=pd.to_numeric(pd.Series([r.get("human_"+d)]),errors="coerce").iloc[0]
    vals[d]=st.slider(d.replace("_"," ").title(),1,5,int(old) if pd.notna(old) else 3)
if st.button("Save human scores", type="primary"):
    for d,v in vals.items(): df.loc[idx,"human_"+d]=v
    df.to_csv(PATH,index=False)
    st.success("Saved")
done=pd.to_numeric(df["human_relevance"],errors="coerce").notna().sum()
st.sidebar.metric("Scored",f"{done}/{len(df)}")
