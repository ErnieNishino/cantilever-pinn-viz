# PINN Cantilever Beam Deflection

[中文说明](README.md)

This project uses DeepXDE + PyTorch to train a PINN (Physics-Informed Neural Network) for solving the Euler-Bernoulli cantilever beam equation, and generates an interactive web visualization page.

## Features

- PINN training pipeline constrained by physical equations (two-stage optimization: Adam + L-BFGS)
- Comparison between analytical solution and PINN prediction
- Automatic reporting of error metrics (relative L2 error) and runtime
- Browser-based interactive visualization (deflection curve, error curve, loss history)
- Modular project structure: config, physics, training, visualization, and entry point are decoupled

## Project Structure

```text
testPINN/
├─ main.py                   # Entry point
├─ dde_setup.py              # DeepXDE backend environment setup
├─ config.py                 # Project configuration (physical params / training params / output names)
├─ physics.py                # Equation, analytical solution, geometry domain, and boundary conditions
├─ training.py               # Model building, training, prediction, and metric collection
├─ visualization.py          # Generates cantilever_data.js and final HTML
├─ cantilever_template.html  # Visualization template
├─ cantilever_style.css      # Page styles
├─ cantilever_app.js         # Interaction logic and chart rendering
├─ requirements.txt          # Python dependencies
└─ .gitignore
```

## Requirements

- Python 3.10+
- A virtual environment is recommended (venv or conda)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Run in the project directory:

```bash
python main.py
```

After running, the script will:

1. Train the PINN model and print error metrics and runtime.
2. Generate `cantilever_data.js` (frontend data file).
3. Generate `cantilever_pinn_viz.html` from `cantilever_template.html`.
4. Automatically open the result in your browser.

## Output Files

- `cantilever_data.js`: exported curve data after training (auto-generated)
- `cantilever_pinn_viz.html`: visualization page (auto-generated)

## Customization

- Tune physical and training parameters: edit `config.py`
- Modify PDE/boundary conditions: edit `physics.py`
- Adjust training strategy: edit `training.py`
- Modify page structure: edit `cantilever_template.html`
- Modify visual styles: edit `cantilever_style.css`
- Modify interactions and charts: edit `cantilever_app.js`

## License

This project is open-sourced under the [MIT License](LICENSE).
