"""Simple CLI with deterministic synthetic demonstration."""
import argparse, csv, json, random
from datetime import date, timedelta
from pathlib import Path
from .core import read_csv, analyze

def demo(path, days=180):
    if days < 30: raise ValueError("Use at least 30 days")
    rng=random.Random(42)
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow(["date","inflow_m3_d"])
        for i in range(days):
            mean=115 if i<days//3 else (168 if i<2*days//3 else 133)
            writer.writerow([(date(2024,1,1)+timedelta(days=i)).isoformat(),
                             round(max(0,mean+rng.gauss(0,6)),3)])

def main():
    p=argparse.ArgumentParser(description="MineWaterWatch — research screening only")
    sub=p.add_subparsers(dest="cmd",required=True)
    d=sub.add_parser("demo")
    d.add_argument("--output",default="examples/demo.csv")
    d.add_argument("--days",type=int,default=180)
    a=sub.add_parser("analyze")
    a.add_argument("csv_file")
    a.add_argument("--out",default="results")
    a.add_argument("--threshold",type=float)
    a.add_argument("--min-segment",type=int,default=10)
    a.add_argument("--penalty",type=float)
    args=p.parse_args()
    if args.cmd=="demo":
        demo(args.output,args.days)
        print("Wrote synthetic CSV:",args.output)
    else:
        result=analyze(read_csv(args.csv_file),args.threshold,args.min_segment,args.penalty)
        out=Path(args.out)
        out.mkdir(parents=True,exist_ok=True)
        (out/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print("Saved:",out/"summary.json")

if __name__=="__main__":
    main()
