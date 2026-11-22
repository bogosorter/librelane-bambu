import json
from pathlib import Path

from librelane.flows.flow import Flow, FlowError
from librelane.state.state import State
from librelane.steps.step import Step

from .bambu_step import BambuStep

Classic = Flow.factory.get("Classic")
assert Classic is not None


@Flow.factory.register()
class BambuFlow(Classic):
    """
    A custom LibreLane flow that introduces a C to Verilog step in the Classic
    flow.
    """

    Steps = [BambuStep] + Classic.Steps

    def __init__(self, config_path, **kwargs):

        # This flow receives as argument a tuple (configuration_path,), which
        # should be passed onto the __init__ of the Classic flow. Classic will
        # read this file and use its parent directory as the design directory.
        # However, Classic is prepared only for Verilog to ASIC compilation,and
        # requires the VERILOG_FILES variable to be set in the configuration
        # file. To prevent the cumbersome solution of requiring the user to
        # supply an empty list of Verilog files, we read the configuration file
        # and create the variable with an empty list here. Another solution
        # would be to rewrite the Classic flow, but that would prevent upstream
        # changes from propagating into this flow.

        # Read the configuration
        config_path = Path(config_path[0])
        with open(config_path) as f:
            config = json.load(f)

        # Set the VERILOG_FILES variable
        if "VERILOG_FILES" in config:
            raise FlowError("variable VERILOG_FILES should be set by the flow itself, please remove it from the configuration")
        config["VERILOG_FILES"] = []

        # Without the path from the configuration file, LibreLane doesn't know
        # which directory to run the flow in
        kwargs["design_dir"] = str(config_path.parent)

        super().__init__(config, **kwargs)

    def run(
        self,
        initial_state: State,
        **kwargs,
    ) -> tuple[State, list[Step]]:

        # The outputs of the Bambu step have to later be used by the Classic
        # flow, supplied in the VERILOG_FILES variable. We therefore have to
        # known the step_dir, which is only known after running the step. As
        # such, the step is run separately from the other steps in the Classic
        # flow.

        self.set_max_stage_count(len(self.Steps))
        self.start_stage("Bambu")
        bambu_step = BambuStep(self.config, state_in=initial_state)
        self.start_step(bambu_step)
        self.end_stage()

        # Point the VERILOG_FILES variable at the files created by Bambu
        name = self.config["DESIGN_NAME"]
        step_dir = Path(bambu_step.step_dir)
        self.config = self.config.copy(VERILOG_FILES=[
            str(step_dir / (name + '.v')),
            str(step_dir / "panda_libtech.v")
        ])

        # Since we have already run the Bambu step, we have to skip it when
        # calling the super flow. An alternative would be to not include it in
        # the steps list at all, but that would also dodge the verification of
        # the configuration argument by LibreLane, which we'd like to keep.
        skip = list(kwargs.pop("skip", None) or [])
        skip.append(bambu_step.id)

        return super().run(initial_state, skip=skip, **kwargs)
