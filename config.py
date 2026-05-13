from dataclasses import dataclass


@dataclass(frozen=True)
class BeamParams:
    length: float = 1.0
    flexural_rigidity: float = 1.0
    distributed_load: float = 1.0


@dataclass(frozen=True)
class TrainingConfig:
    num_domain: int = 64
    num_boundary: int = 2
    num_test: int = 200
    hidden_size: int = 64
    hidden_layers: int = 4
    adam_lr: float = 1e-3
    adam_iterations: int = 10000
    loss_weights: tuple[float, float, float, float, float] = (1.0, 10.0, 10.0, 10.0, 10.0)


@dataclass(frozen=True)
class OutputFiles:
    template_html: str = "cantilever_template.html"
    data_js: str = "cantilever_data.js"
    output_html: str = "cantilever_pinn_viz.html"
