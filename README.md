# PINN Cantilever Beam Deflection

[English Version](README.en.md)

使用 DeepXDE + PyTorch 训练 PINN（Physics-Informed Neural Network）求解欧拉-伯努利悬臂梁方程，并生成可交互的前端可视化页面。

## Features

- 基于物理方程约束的 PINN 训练流程（Adam + L-BFGS 两阶段优化）
- 解析解与 PINN 预测对比
- 自动输出误差指标（L2 相对误差）与耗时
- 生成浏览器交互可视化（挠度曲线、误差曲线、损失历史）
- 工程化拆分：配置、物理、训练、可视化、入口解耦

## Project Structure

```text
testPINN/
├─ main.py                   # 入口
├─ dde_setup.py              # DeepXDE 后端环境设置
├─ config.py                 # 项目配置（物理参数/训练配置/输出文件名）
├─ physics.py                # 方程、解析解、几何域与边界条件
├─ training.py               # 模型构建、训练、预测与指标采集
├─ visualization.py          # 生成 cantilever_data.js 与最终 HTML
├─ cantilever_template.html  # 可视化模板
├─ cantilever_style.css      # 页面样式
├─ cantilever_app.js         # 页面交互与图表逻辑
├─ requirements.txt          # Python 依赖
└─ .gitignore
```

## Requirements

- Python 3.10+
- 建议使用虚拟环境（venv 或 conda）

安装依赖：

```bash
pip install -r requirements.txt
```

## Quick Start

在当前目录执行：

```bash
python main.py
```

运行后将会：

1. 完成 PINN 训练并打印误差和耗时。
2. 生成 `cantilever_data.js`（前端数据文件）。
3. 基于 `cantilever_template.html` 生成 `cantilever_pinn_viz.html`。
4. 自动打开浏览器展示结果。

## Output Files

- `cantilever_data.js`：训练后导出的曲线数据（自动生成）
- `cantilever_pinn_viz.html`：可视化页面（自动生成）

## Customization

- 调整物理参数与训练参数：编辑 `config.py`
- 修改 PDE/边界条件：编辑 `physics.py`
- 修改训练策略：编辑 `training.py`
- 修改页面结构：编辑 `cantilever_template.html`
- 修改视觉样式：编辑 `cantilever_style.css`
- 修改交互逻辑与图表：编辑 `cantilever_app.js`

## License

本项目基于 [MIT License](LICENSE) 协议开源。