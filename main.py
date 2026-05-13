from pathlib import Path

from config import BeamParams, OutputFiles, TrainingConfig
from training import build_model, collect_predictions, train_model
from visualization import write_visualization_files


def main() -> None:
    print("=== PINN 悬臂梁挠度预测（含交互可视化）===")

    params = BeamParams()
    cfg = TrainingConfig()
    outputs = OutputFiles()

    model = build_model(params, cfg)
    result = train_model(model, cfg)
    stats = collect_predictions(result, params)

    print("\n===== 训练完成 =====")
    print(f"最大挠度（解析解）: {stats['max_exact']:.6f}")
    print(f"最大挠度（PINN）  : {stats['max_pred']:.6f}")
    print(f"L2 相对误差       : {stats['l2_error']:.2e}")
    print(f"物理仿真总耗时    : {stats['t_total_ms']} ms")
    print(f"PINN 推断耗时     : {stats['t_infer_ms']:.1f} ms")

    out_path = write_visualization_files(Path(__file__).resolve().parent, outputs, stats, auto_open=True)
    print(f"\n可视化已保存至: {out_path.resolve()}")
    print("正在自动打开浏览器...")


if __name__ == "__main__":
    main()
