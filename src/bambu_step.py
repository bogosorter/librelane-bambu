import time
from pathlib import Path as PPath

from librelane.common.types import Path
from librelane.config.variable import Variable
from librelane.state.state import State
from librelane.steps.step import MetricsUpdate, Step, ViewsUpdate

bambu = PPath("~/Downloads/bambu-2026.11.AppImage").expanduser()

@Step.factory.register()
class BambuStep(Step):
    id = "Bambu.Step"
    name = "Bambu Step"
    inputs = []
    outputs = []
    config_vars = [
        Variable("C_FILE", Path, "C source file for Bambu")
    ]

    def run(self, state_in: State, **kwargs) -> tuple[ViewsUpdate, MetricsUpdate]:
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
