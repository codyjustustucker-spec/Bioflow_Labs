from __future__ import annotations

from dataclasses import replace
from typing import Optional

from .state import Params, State
from .engine import step, compute_derived


class SimOrchestrator:
    """
    Owns params + state + run control.
    UI talks to this, not to engine.step directly.
    Deterministic: exactly one step per tick, fixed ordering.
    """

    def __init__(self, params: Optional[Params] = None, initial: Optional[State] = None) -> None:
        self.params: Params = params or Params()
        self._initial: State = compute_derived(
            initial or self._default_initial(self.params), self.params)
        self.state: State = self._initial
        self.paused: bool = True

    @staticmethod
    def _default_initial(p: Params) -> State:
        # Reasonable starting split; must sum to total_volume_ml
        V_pool = 0.10 * p.total_volume_ml
        V_art = 0.20 * p.total_volume_ml
        V_ven = p.total_volume_ml - V_art - V_pool
        return State(V_art_ml=V_art, V_ven_ml=V_ven, V_pool_ml=V_pool)

    # --- Control hooks ---

    def play(self) -> None:
        self.paused = False

    def pause(self) -> None:
        self.paused = True

    def reset(self, *, keep_params: bool = True) -> None:
        p = self.params if keep_params else Params()
        self.params = p
        self._initial = compute_derived(self._default_initial(p), p)
        self.state = self._initial
        self.paused = True

    def soft_reset(self) -> None:
        was_paused = self.paused
        self.state = compute_derived(
            self._default_initial(self.params), self.params)
        self.paused = was_paused

    # --- Deterministic stepping ---

    def tick(self, n: int = 1) -> State:
        """
        Advance simulation by n fixed steps (dt).
        Deterministic ordering:
          1) compute_derived inside step
          2) apply transfers
          3) clamp/conserve
          4) compute_derived again
        """
        if self.paused:
            return self.state

        s = self.state
        for _ in range(max(0, n)):
            s = step(s, self.params)

        self.state = s
        return s

    # --- Convenience: update parameters safely ---

    def update_params(self, **kwargs) -> None:
        # Clamp core stability ranges here (single source of truth)
        if "dt" in kwargs:
            kwargs["dt"] = max(0.001, min(0.05, float(kwargs["dt"])))

        if "peripheral_resistance" in kwargs:
            kwargs["peripheral_resistance"] = max(
                0.05, min(20.0, float(kwargs["peripheral_resistance"])))

        if "arterial_compliance" in kwargs:
            kwargs["arterial_compliance"] = max(
                0.1, min(20.0, float(kwargs["arterial_compliance"])))

        if "venous_pooling_target" in kwargs:
            kwargs["venous_pooling_target"] = max(
                0.0, min(0.6, float(kwargs["venous_pooling_target"])))

        if "hr_bpm" in kwargs:
            kwargs["hr_bpm"] = max(20.0, min(250.0, float(kwargs["hr_bpm"])))

        if "stroke_volume_ml" in kwargs:
            kwargs["stroke_volume_ml"] = max(
                0.0, min(400.0, float(kwargs["stroke_volume_ml"])))

        self.params = replace(self.params, **kwargs)
        self.state = compute_derived(self.state, self.params)

    def set_params(self, params: Params) -> None:
        self.params = params
        self.state = compute_derived(self.state, self.params)

    def baseline_params(self) -> Params:
        return Params()  # your canonical baseline
