from dataclasses import dataclass
import time

import dde_setup
import deepxde as dde
import numpy as np

from config import BeamParams, TrainingConfig
from physics import beam_equation, create_geometry_and_bcs, exact_solution


@dataclass(frozen=True)
class TrainResult:
    model: dde.Model
    losshistory: object
    t_adam: float
    t_lbfgs: float


def build_model(params: BeamParams, cfg: TrainingConfig) -> dde.Model:
    geom, bcs = create_geometry_and_bcs(params)
    data = dde.data.PDE(
        geom,
        beam_equation(params),
        bcs,
        num_domain=cfg.num_domain,
        num_boundary=cfg.num_boundary,
        solution=lambda x: exact_solution(x, params),
        num_test=cfg.num_test,
    )

    net = dde.nn.FNN(
        [1] + [cfg.hidden_size] * cfg.hidden_layers + [1],
        activation="tanh",
        kernel_initializer="Glorot normal",
    )
    return dde.Model(data, net)


def train_model(model: dde.Model, cfg: TrainingConfig) -> TrainResult:
    model.compile("adam", lr=cfg.adam_lr, metrics=["l2 relative error"], loss_weights=list(cfg.loss_weights))
    print("第一阶段：Adam 优化器训练中...")
    t0 = time.time()
    losshistory, _ = model.train(iterations=cfg.adam_iterations)
    t_adam = time.time() - t0

    print("第二阶段：L-BFGS 精调中...")
    model.compile("L-BFGS", metrics=["l2 relative error"], loss_weights=list(cfg.loss_weights))
    t1 = time.time()
    losshistory, _ = model.train()
    t_lbfgs = time.time() - t1

    return TrainResult(model=model, losshistory=losshistory, t_adam=t_adam, t_lbfgs=t_lbfgs)


def collect_predictions(result: TrainResult, params: BeamParams, n_plot: int = 200) -> dict:
    x_plot = np.linspace(0, params.length, n_plot).reshape(-1, 1)

    infer_start = time.time()
    y_pred = result.model.predict(x_plot).flatten()
    t_infer_ms = (time.time() - infer_start) * 1000

    y_exact = exact_solution(x_plot, params).flatten()
    x_flat = x_plot.flatten()

    l2_error = float(np.linalg.norm(y_pred - y_exact) / np.linalg.norm(y_exact))
    max_exact = float(np.max(np.abs(y_exact)))
    max_pred = float(np.max(np.abs(y_pred)))

    pinn_ratio = []
    for i in range(len(y_exact)):
        if abs(y_exact[i]) > 1e-12:
            pinn_ratio.append(float(y_pred[i] / y_exact[i]))
        else:
            pinn_ratio.append(1.0)

    loss_steps = [int(s) for s in result.losshistory.steps]
    loss_train = [float(sum(row)) for row in result.losshistory.loss_train]

    return {
        "x_flat": x_flat,
        "y_exact": y_exact,
        "y_pred": y_pred,
        "pinn_ratio": pinn_ratio,
        "loss_steps": loss_steps,
        "loss_train": loss_train,
        "l2_error": l2_error,
        "max_exact": max_exact,
        "max_pred": max_pred,
        "t_total_ms": int((result.t_adam + result.t_lbfgs) * 1000),
        "t_infer_ms": t_infer_ms,
    }
