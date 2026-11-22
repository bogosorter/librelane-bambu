import os

from librelane.common.types import Path as PathType
from librelane.config.variable import Variable
from librelane.state.state import State
from librelane.steps.step import MetricsUpdate, Step, StepError, ViewsUpdate


@Step.factory.register()
class BambuStep(Step):
    """
    A custom LibreLane step that transforms C source files into Verilog using
    Bambu.
    - `C_FILE`: C source file for transformation
    """

    id = "bambu"
    name = "Bambu"
    inputs = []
    outputs = []
    config_vars = [
        Variable("C_FILE", PathType, "C source file")
    ]

    def run(self, state_in: State, **kwargs) -> tuple[ViewsUpdate, MetricsUpdate]:
        # This step is essentially a wrapper around Bambu. It requires an
        # environment variable that points at the Bambu installation path
        bambu = os.environ.get("BAMBU_PATH")
        if bambu is None:
            raise StepError("environment variable BAMBU_PATH is not set (see installation instructions in readme)")

        name = self.config["DESIGN_NAME"]
        source = self.config["C_FILE"]
        clock_period = self.config["CLOCK_PERIOD"]
        clock_port = self.config["CLOCK_PORT"]

        # Actually call Bambu
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
