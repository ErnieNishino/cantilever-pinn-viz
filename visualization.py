import json
import webbrowser
from pathlib import Path

from config import OutputFiles


def _to_js_array(values, precision: int):
    return json.dumps([round(float(v), precision) for v in values])


def write_visualization_files(base_dir: Path, outputs: OutputFiles, stats: dict, auto_open: bool = True) -> Path:
    template_path = base_dir / outputs.template_html
    data_path = base_dir / outputs.data_js
    out_path = base_dir / outputs.output_html

    x_js = _to_js_array(stats["x_flat"], 6)
    y_exact_js = _to_js_array(stats["y_exact"], 10)
    y_pred_js = _to_js_array(stats["y_pred"], 10)
    pinn_ratio_js = _to_js_array(stats["pinn_ratio"], 8)
    loss_steps_js = json.dumps(stats["loss_steps"])
    loss_vals_js = _to_js_array(stats["loss_train"], 12)

    data_js = "\n".join(
        [
            f"const xData = {x_js};",
            f"const yExact = {y_exact_js};",
            f"const yPred = {y_pred_js};",
            f"const pinnRatio = {pinn_ratio_js};",
            f"const lossSteps = {loss_steps_js};",
            f"const lossVals = {loss_vals_js};",
        ]
    ) + "\n"
    data_path.write_text(data_js, encoding="utf-8")

    template_html = template_path.read_text(encoding="utf-8")
    html = (
        template_html.replace("{{HDR_PHYS}}", f"{stats['max_exact'] * 1000:.3f} mm")
        .replace("{{HDR_SURR}}", f"{stats['max_pred'] * 1000:.3f} mm")
        .replace("{{SIM_MS}}", f"{stats['t_total_ms']} ms")
        .replace("{{INFER_MS}}", f"{stats['t_infer_ms']:.1f} ms")
    )
    out_path.write_text(html, encoding="utf-8")

    if auto_open:
        webbrowser.open(out_path.resolve().as_uri())

    return out_path
