import csv
from api.predict import score

rows = list(csv.DictReader(open("sample_transactions.csv")))
inputs = [{k: v for k, v in r.items() if k != "Class"} for r in rows]
for r, s in zip(rows, score(inputs)):
    print("actual:", r["Class"], "->", s)