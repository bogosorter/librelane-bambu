import time
from typing import List, Tuple
from librelane.flows import Flow
from librelane.state import State
from librelane.steps import Step, ViewsUpdate, MetricsUpdate
from librelane.config import Variable
from librelane.common import Path

from pathlib import Path as PPath
bambu = PPath("~/Downloads/bambu-2026.11.AppImage").expanduser()

Classic = Flow.factory.get("Classic")

@Step.factory.register()
class BambuStep(Step):
    id = "Bambu.Step"
    name = "Bambu Step"
    inputs = []
    outputs = []
    config_vars = [
        Variable("C_FILE", Path, "C source file for Bambu")
    ]

    def run(self, state_in: State, **kwargs) -> Tuple[ViewsUpdate, MetricsUpdate]:
        name = self.config["DESIGN_NAME"]
        source = self.config["C_FILE"]
        clock_period = self.config["CLOCK_PERIOD"]
        clock_port = self.config["CLOCK_PORT"]
        self.run_subprocess([
            bambu, source,
            f"--top-fname={name}",
            f"--clock-period={clock_period}",
            f"--clock-name={clock_port}",
            "--disable-reg-init-value",
            "-v4"
        ], cwd=self.step_dir)
        time.sleep(2)
        return {}, {}

class CustomFlow(Classic):
    Steps = [BambuStep] + Classic.Steps

    def run(
        self,
        initial_state: State,
        **kwargs,
    ) -> Tuple[State, List[Step]]:

        self.set_max_stage_count(len(self.Steps))
        self.start_stage("Bambu Stage")
        bambu_step = BambuStep(self.config, state_in=initial_state)
        self.start_step(bambu_step)
        self.end_stage()

        out = PPath(bambu_step.step_dir)
        self.config = self.config.copy(VERILOG_FILES=[str(out / "icrc1.v"), str(out / "panda_libtech.v")])
        print(self.config)
        return super().run(initial_state, skip=["Bambu.Step"], **kwargs)
