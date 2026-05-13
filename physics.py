from collections.abc import Callable

import dde_setup
import deepxde as dde
import numpy as np

from config import BeamParams


def exact_solution(x: np.ndarray, params: BeamParams) -> np.ndarray:
    L = params.length
    EI = params.flexural_rigidity
    q = params.distributed_load
    return (q / (24.0 * EI)) * x**2 * (x**2 - 4.0 * L * x + 6.0 * L**2)


def beam_equation(params: BeamParams) -> Callable:
    EI = params.flexural_rigidity
    q = params.distributed_load

    def pde(x, y):
        dy_x = dde.grad.jacobian(y, x, i=0, j=0)
        dy_xx = dde.grad.jacobian(dy_x, x, i=0, j=0)
        dy_xxx = dde.grad.jacobian(dy_xx, x, i=0, j=0)
        dy_xxxx = dde.grad.jacobian(dy_xxx, x, i=0, j=0)
        return EI * dy_xxxx - q

    return pde


def create_geometry_and_bcs(params: BeamParams):
    geom = dde.geometry.Interval(0, params.length)

    def on_left(x, on_boundary):
        return on_boundary and np.isclose(x[0], 0.0)

    def on_right(x, on_boundary):
        return on_boundary and np.isclose(x[0], params.length)

    bc_disp = dde.icbc.DirichletBC(geom, lambda _: 0.0, on_left)

    def slope(x, y, _):
        return dde.grad.jacobian(y, x, i=0, j=0)

    bc_slope = dde.icbc.OperatorBC(geom, slope, on_left)

    def bending_moment(x, y, _):
        dy_x = dde.grad.jacobian(y, x, i=0, j=0)
        dy_xx = dde.grad.jacobian(dy_x, x, i=0, j=0)
        return dy_xx

    bc_moment = dde.icbc.OperatorBC(geom, bending_moment, on_right)

    def shear_force(x, y, _):
        dy_x = dde.grad.jacobian(y, x, i=0, j=0)
        dy_xx = dde.grad.jacobian(dy_x, x, i=0, j=0)
        dy_xxx = dde.grad.jacobian(dy_xx, x, i=0, j=0)
        return dy_xxx

    bc_shear = dde.icbc.OperatorBC(geom, shear_force, on_right)
    return geom, [bc_disp, bc_slope, bc_moment, bc_shear]
