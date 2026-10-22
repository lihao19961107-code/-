# MineWaterWatch

**Open-source Python toolkit for exploratory daily mine-water inflow screening.**

**Status:** v0.1.0 research preview. No external adoption, validation, or production-safety claims are made.

## Capabilities

- Validate daily CSV observations and detect missing calendar dates
- Exact dynamic-programming segmentation of piecewise-constant means using SSE plus a penalty
- Identify strictly above-threshold episodes and cumulative excess volume
- Reproducible synthetic CSV demonstration and automated tests
- Export machine-readable JSON for independent review

## Install and run

Requires Python 3.10+.

```bash
python -m pip install -e .
minewaterwatch demo --output examples/demo.csv
minewaterwatch analyze examples/demo.csv --threshold 150 --min-segment 10 --out results
python -m pip install pytest
python -m pytest -q
```

Required CSV columns: `date,inflow_m3_d`, with ISO dates and nonnegative finite daily-equivalent inflow in m³/day. See [中文说明](README.zh-CN.md).

The algorithm minimizes the sum of within-segment squared residuals plus one penalty for every extra segment. Segment length counts observed rows. The default penalty uses the median absolute deviation of successive differences. Segmentation costs O(n²) operations and should be sensitivity-tested for long, autocorrelated or incomplete time series.

**Important:** These are statistical candidate changes, not evidence of physical water-flow pathways. Missing days are not imputed. This project must not be used for real-time mine safety alerts, regulatory compliance, or operational flood prevention. The demo is synthetic, not field validation.

## Open source

The project is maintained as an early-stage research utility; contributions and reproducible bug reports are welcome. License: MIT.
