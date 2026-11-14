from pathlib import Path as PPath

from librelane.flows.flow import Flow
from librelane.state.state import State
from librelane.steps.step import Step

from .bambu_step import BambuStep

Classic = Flow.factory.get("Classic")
assert Classic is not None

class BambuFlow(Classic):
    Steps = [BambuStep] + Classic.Steps

    def run(
        self,
        initial_state: State,
        **kwargs,
    ) -> tuple[State, list[Step]]:

        self.set_max_stage_count(len(self.Steps))
        self.start_stage("Bambu Stage")
        bambu_step = BambuStep(self.config, state_in=initial_state)
        self.start_step(bambu_step)
        self.end_stage()

        out = PPath(bambu_step.step_dir)
        name = self.config["DESIGN_NAME"]
        self.config = self.config.copy(VERILOG_FILES=[str(out / (name + '.v')), str(out / "panda_libtech.v")])
        print(self.config)
        return super().run(initial_state, skip=["Bambu.Step"], **kwargs)
