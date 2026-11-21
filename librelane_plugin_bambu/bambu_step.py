import os
import sys
from pathlib import Path

from librelane.common.types import Path as PathType
from librelane.config.variable import Variable
from librelane.state.state import State
from librelane.steps.step import MetricsUpdate, Step, StepError, ViewsUpdate

MAIN = sys.modules["__main__"].__file__
assert MAIN is not None
MAIN_DIR = Path(MAIN).resolve().parent

@Step.factory.register()
class BambuStep(Step):
    id = "bambu"
    name = "Bambu"
    inputs = []
    outputs = []
    config_vars = [
        Variable("C_FILE", PathType, "C source file for Bambu")
    ]

    def run(self, state_in: State, **kwargs) -> tuple[ViewsUpdate, MetricsUpdate]:
        bambu = os.environ.get("BAMBU_PATH")
        if bambu is None:
            raise StepError("BAMBU_PATH is not set (see readme)")

        print("got path", bambu)

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

        # TODO: Missing elements in return values?
        return {}, {}
