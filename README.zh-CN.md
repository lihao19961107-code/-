# MineWaterWatch — 矿井涌水量分析工具

这是一个早期研究版开源 Python 工具，用于日涌水量数据的质量检查、统计变化点识别和超限持续性统计。

**本程序不能作为矿井安全报警、现场防治水决策或监管合规依据。** 示例数据全部为随机生成的合成数据，不能当作真实观测或工程验证。

## 快速使用

```bash
python -m pip install -e .
minewaterwatch demo --output examples/demo.csv
minewaterwatch analyze examples/demo.csv --threshold 150 --out results
```

分析结果保存在 `results/summary.json`，包含变化日期、分段均值、缺测日期和超限事件。阈值必须根据具体工程背景由专业人员确定。

欢迎提供不涉及保密信息的错误报告、功能需求和可复现测试。

## Python 接口输入校验

直接调用 `analyze(observations, ...)` 时，日期必须为 `datetime.date` 类型且严格递增、不得重复，涌水量必须是有限的非负实数。非法输入会返回明确的 `ValueError`；通过 `read_csv(path)` 读取的 CSV 数据会先进行日期排序与重复检查。缺测日期只做标记，不自动填补。
