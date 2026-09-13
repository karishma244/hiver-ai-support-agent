import streamlit as st
import pandas as pd
from src.agent import SupportAgent

st.set_page_config(page_title="AppleSupport AI Agent", page_icon="🍎", layout="centered")
st.title("🍎 AppleSupport AI Support Agent")
st.caption("Intent classification • grounded draft • selective auto-handle/escalation")

@st.cache_resource
def load_agent():
    g=pd.read_csv("data/golden_review.csv")
    h=pd.read_csv("data/historical_resolutions.csv")
    return SupportAgent().fit(g,h)

agent=load_agent()
msg=st.text_area("Incoming customer message", height=120, value="My iPhone battery is draining very fast after the latest iOS update.")
if st.button("Run agent", type="primary"):
    out=agent.handle(msg)
    c1,c2=st.columns(2)
    c1.metric("Intent", out["intent"])
    c2.metric("Confidence", out["intent_confidence"])
    st.subheader("Draft reply")
    st.write(out["draft_reply"])
    if out["action"]=="auto_handle":
        st.success("AUTO-HANDLE")
    else:
        st.warning("ESCALATE TO HUMAN")
    st.write("**Reason:**", out["reason"])
    st.write("**Grounding similarity:**", out["grounding_similarity"])
