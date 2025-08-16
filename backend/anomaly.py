from sklearn.ensemble import IsolationForest

def detect_anomalies(log_df):
    if log_df.empty:
        return []
    counts = log_df.groupby("timestamp").size().values.reshape(-1, 1)
    clf = IsolationForest(contamination=0.05, random_state=42)
    preds = clf.fit_predict(counts)
    return preds
