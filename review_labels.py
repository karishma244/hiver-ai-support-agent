import streamlit as st
import pandas as pd
from pathlib import Path

PATH=Path("data/golden_review.csv")
df=pd.read_csv(PATH)
INTENTS=sorted(df["intent"].unique())

st.set_page_config(page_title="Golden Set Review", layout="wide")
st.title("Golden set human review")
st.caption("Review each row. Save after edits. When finished, set label_status to HUMAN_REVIEWED.")

idx=st.number_input("Row", min_value=1, max_value=len(df), value=1, step=1)-1
row=df.iloc[idx]
st.progress((idx+1)/len(df))
st.code(row["text"], language=None)
intent=st.selectbox("Intent", INTENTS, index=INTENTS.index(row["intent"]))
esc=st.checkbox("Escalate", value=str(row["escalate"]).lower()=="true")
notes=st.text_input("Notes", value="" if pd.isna(row.get("notes","")) else str(row.get("notes","")))
col1,col2,col3=st.columns(3)
if col1.button("Save"):
    df.loc[idx,"intent"]=intent
    df.loc[idx,"escalate"]=str(bool(esc)).lower()
    df.loc[idx,"notes"]=notes
    df.loc[idx,"label_status"]="HUMAN_REVIEWED"
    df.to_csv(PATH,index=False)
    st.success("Saved")
if col2.button("Previous") and idx>0:
    st.session_state["jump"]=idx
if col3.button("Next") and idx<len(df)-1:
    st.session_state["jump"]=idx+2
done=(df["label_status"]=="HUMAN_REVIEWED").sum()
st.sidebar.metric("Reviewed", f"{done}/{len(df)}")
st.sidebar.write("After all rows are reviewed, rerun:")
st.sidebar.code("python -m src.evaluate")
