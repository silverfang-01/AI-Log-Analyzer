import re
import pandas as pd

def parse_logs(file_path):
    rows = []
    # 2025-08-15 12:30:01 ERROR Something...
    pattern = r"(?P<timestamp>\S+\s+\S+)\s+(?P<level>INFO|ERROR|WARN)\s+(?P<message>.*)"
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = re.match(pattern, line.strip())
            if m:
                d = m.groupdict()
                d["full"] = f'{d["timestamp"]} {d["level"]} {d["message"]}'
                rows.append(d)
    return pd.DataFrame(rows)
