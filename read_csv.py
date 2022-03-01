import pandas as pd

col_list = ["Name"]
df = pd.read_csv(("mitre attck software - Sheet1.csv"), usecols=col_list)

print(df["Name"])