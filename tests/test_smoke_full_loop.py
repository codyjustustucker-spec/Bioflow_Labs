from bioflow.sim.orchestrator import SimOrchestrator


def test_smoke_runs_and_is_finite():
    sim = SimOrchestrator()
    sim.play()

    # Run ~10 seconds
    steps = int(10.0 / sim.params.dt)
    for _ in range(steps):
        s = sim.tick()

        # Must remain finite and non-negative
        assert s.V_art_ml >= 0.0
        assert s.V_ven_ml >= 0.0
        assert s.V_pool_ml >= 0.0
        assert s.P_art_mmHg >= 0.0
        assert s.P_ven_mmHg >= 0.0
        assert s.P_pool_mmHg >= 0.0

    total = s.V_art_ml + s.V_ven_ml + s.V_pool_ml
    assert abs(total - sim.params.total_volume_ml) < 1e-6
