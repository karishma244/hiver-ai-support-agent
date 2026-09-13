import argparse,json,pandas as pd
from .agent import SupportAgent
p=argparse.ArgumentParser()
p.add_argument("message",nargs="+")
a=p.parse_args()
g=pd.read_csv("data/golden_review.csv")
h=pd.read_csv("data/historical_resolutions.csv")
agent=SupportAgent().fit(g,h)
print(json.dumps(agent.handle(" ".join(a.message)),indent=2))
