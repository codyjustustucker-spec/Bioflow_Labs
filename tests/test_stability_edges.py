from bioflow.sim.orchestrator import SimOrchestrator
from bioflow.sim.validate import assess


def test_extremes_do_not_crash():
    sim = SimOrchestrator()
    sim.play()

    sim.update_params(hr_bpm=250, stroke_volume_ml=300, peripheral_resistance=0.05,
                      arterial_compliance=0.1, venous_pooling_target=0.6)

    for _ in range(2000):
        s = sim.tick()
        h = assess(s, sim.params)
        # Allowed to WARN, but must stay finite
        assert h.ok or h.level == "WARN"
