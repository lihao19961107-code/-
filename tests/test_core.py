from datetime import date, timedelta
from minewaterwatch.core import analyze, read_csv

def observations(values):
    return [(date(2024,1,1)+timedelta(days=i),v) for i,v in enumerate(values)]

def test_change_point():
    result=analyze(observations([10.]*20+[30.]*20),min_segment=5)
    assert result["change_dates"]==["2024-01-21"]

def test_constant_series():
    assert analyze(observations([10.]*50),min_segment=5)["change_dates"]==[]

def test_exceedance():
    result=analyze(observations([5.,12.,13.,5.]),threshold=10,min_segment=2)
    assert result["exceedance_events"][0]["days"]==2
    assert result["exceedance_events"][0]["cumulative_excess_m3"]==5

def test_read_csv(tmp_path):
    p=tmp_path/"data.csv"
    p.write_text("date,inflow_m3_d\n2024-01-01,4\n2024-01-02,5\n")
    assert len(read_csv(p))==2
