"""Retrospective research screening; not for live mine safety decisions."""
import csv, math, statistics
from datetime import date, timedelta

def read_csv(path):
    observations = []
    seen = set()
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not {"date", "inflow_m3_d"}.issubset(reader.fieldnames or []):
            raise ValueError("Required columns: date,inflow_m3_d")
        for row in reader:
            day = date.fromisoformat(row["date"].strip())
            val = float(row["inflow_m3_d"])
            if day in seen or not math.isfinite(val) or val < 0:
                raise ValueError("Duplicate date or invalid inflow")
            seen.add(day)
            observations.append((day, val))
    if not observations:
        raise ValueError("Empty dataset")
    return sorted(observations)

def analyze(observations, threshold=None, min_segment=10, penalty=None):
    if min_segment < 2 or len(observations) < min_segment:
        raise ValueError("Insufficient observations or invalid segment length")
    y = [x[1] for x in observations]
    n = len(y)
    if penalty is None:
        diffs = [b-a for a,b in zip(y,y[1:])]
        med = statistics.median(diffs)
        mad = statistics.median(abs(x-med) for x in diffs)
        sigma = max(1.4826*mad/math.sqrt(2), .02*max(statistics.median(y),1))
        penalty = 3*sigma*sigma*math.log(n)
    if not math.isfinite(penalty) or penalty <= 0:
        raise ValueError("Penalty must be positive and finite")
    s, q = [0.], [0.]
    for value in y:
        s.append(s[-1]+value)
        q.append(q[-1]+value*value)
    def cost(a,b):
        return max(0.,q[b]-q[a]-(s[b]-s[a])**2/(b-a))
    dp = [float("inf")]*(n+1)
    prev = [-1]*(n+1)
    dp[0] = -penalty
    for end in range(min_segment,n+1):
        for start in range(end-min_segment+1):
            candidate = dp[start]+cost(start,end)+penalty
            if candidate < dp[end]:
                dp[end],prev[end] = candidate,start
    intervals=[]
    end=n
    while end:
        start=prev[end]
        if start < 0: raise RuntimeError("Segmentation failed")
        intervals.append((start,end))
        end=start
    intervals.reverse()
    segments=[{"start":observations[a][0].isoformat(),
               "end":observations[b-1][0].isoformat(),
               "mean_m3_d":round((s[b]-s[a])/(b-a),6),
               "observed_days":b-a} for a,b in intervals]
    observed_days={d for d,_ in observations}
    day=observations[0][0]
    gaps=[]
    while day<=observations[-1][0]:
        if day not in observed_days: gaps.append(day.isoformat())
        day+=timedelta(days=1)
    events=[]
    if threshold is not None:
        if not math.isfinite(threshold) or threshold<0: raise ValueError("Invalid threshold")
        running=[]
        def flush():
            if running:
                events.append({"start":running[0][0].isoformat(),
                    "end":running[-1][0].isoformat(),"days":len(running),
                    "peak_m3_d":max(v for _,v in running),
                    "cumulative_excess_m3":round(sum(v-threshold for _,v in running),6)})
                running.clear()
        for d,v in observations:
            if v>threshold:
                if running and (d-running[-1][0]).days!=1: flush()
                running.append((d,v))
            else: flush()
        flush()
    return {"observations":n,"threshold_m3_d":threshold,
       "penalty":penalty,"min_segment":min_segment,
       "change_dates":[observations[a][0].isoformat() for a,_ in intervals[1:]],
       "segments":segments,"missing_dates":gaps,"exceedance_events":events,
       "note":"Exploratory statistical screening only; synthetic demonstration is not field validation."}
