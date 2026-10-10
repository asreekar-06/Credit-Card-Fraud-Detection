from http.server import BaseHTTPRequestHandler
import json, os
import joblib
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = joblib.load(os.path.join(BASE, "model", "fraud_model.joblib"))
MODEL, SCALER, COLS = ART["model"], ART["scaler"], ART["columns"]
LOW, HIGH = ART["low"], ART["high"]


def score(rows):
    df = pd.DataFrame(rows)
    missing = [c for c in COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing[:5]}")
    df = df[COLS].astype(float)
    df[["Time", "Amount"]] = SCALER.transform(df[["Time", "Amount"]])
    out = []
    for p in MODEL.predict_proba(df)[:, 1]:
        if p >= HIGH:
            decision = "fraud"
        elif p <= LOW:
            decision = "genuine"
        else:
            decision = "review"
        out.append({"probability": round(float(p), 4), "decision": decision})
    return out


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"status": "ok", "low": LOW, "high": HIGH})

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            rows = json.loads(self.rfile.read(n))["rows"]
            if not isinstance(rows, list) or not 1 <= len(rows) <= 5000:
                raise ValueError("Send between 1 and 5000 rows")
            self._send(200, {"results": score(rows), "low": LOW, "high": HIGH})
        except Exception as e:
            self._send(400, {"error": str(e)})