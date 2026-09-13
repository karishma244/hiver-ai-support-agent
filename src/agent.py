import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

RISK_INTENTS={"apple_id_account","app_store_purchases","icloud_backup_storage","device_hardware_damage","general_other"}
DANGER=re.compile(r"swollen|smoke|fire|burn|overheat|very hot|wet|water damage|stolen|fraud|unauthori[sz]ed|charged twice|lost photos|data loss",re.I)
PII=re.compile(r"\b\d{12,16}\b|\b\d{3}-?\d{2}-?\d{4}\b",re.I)

class SupportAgent:
    def __init__(self, confidence_threshold=.38, retrieval_threshold=.08):
        self.confidence_threshold=confidence_threshold
        self.retrieval_threshold=retrieval_threshold
        self.clf=Pipeline([
            ("tfidf",TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)),
            ("lr",LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42))
        ])
        self.reply_vec=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)

    def fit(self,gold_df,hist_df):
        self.clf.fit(gold_df.text,gold_df.intent)
        self.hist=hist_df.reset_index(drop=True)
        self.reply_X=self.reply_vec.fit_transform((self.hist.intent+" "+self.hist.reply).tolist())
        return self

    def predict_intent(self,text):
        probs=self.clf.predict_proba([text])[0]
        i=probs.argmax()
        return self.clf.classes_[i],float(probs[i])

    def retrieve_reply(self,text,intent):
        q=self.reply_vec.transform([intent+" "+text])
        sims=cosine_similarity(q,self.reply_X)[0]
        mask=self.hist.intent.values==intent
        scored=sims.copy(); scored[~mask]=-1
        idx=int(scored.argmax()); sim=float(scored[idx])
        return self.hist.iloc[idx].reply,sim

    def decide_escalation(self,text,intent,confidence,retrieval_sim):
        reasons=[]
        if intent in RISK_INTENTS:
            reasons.append("account/payment/data/hardware/ambiguous intent requires human-safe handling")
        if confidence < self.confidence_threshold:
            reasons.append(f"low intent confidence ({confidence:.2f})")
        if retrieval_sim < self.retrieval_threshold:
            reasons.append(f"weak historical grounding ({retrieval_sim:.2f})")
        if DANGER.search(text):
            reasons.append("safety, fraud, or potential data-loss signal")
        if PII.search(text):
            reasons.append("possible sensitive information")
        return bool(reasons), "; ".join(reasons) if reasons else "high-confidence, low-risk intent with sufficiently similar historical resolution"

    def handle(self,text):
        intent,conf=self.predict_intent(text)
        reply,sim=self.retrieve_reply(text,intent)
        esc,reason=self.decide_escalation(text,intent,conf,sim)
        return {
            "intent":intent,
            "intent_confidence":round(conf,3),
            "draft_reply":reply,
            "grounding_similarity":round(sim,3),
            "action":"escalate" if esc else "auto_handle",
            "reason":reason
        }
