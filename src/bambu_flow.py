from pathlib import Path

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

        # This step has to be executed separately to later use its step_dir
        self.set_max_stage_count(len(self.Steps))
        self.start_stage("Bambu")
        bambu_step = BambuStep(self.config, state_in=initial_state)
        self.start_step(bambu_step)
        self.end_stage()

        # Change the verilog files to point to the files created by bambu
        name = self.config["DESIGN_NAME"]
        output_directory = Path(bambu_step.step_dir)
        self.config = self.config.copy(VERILOG_FILES=[
            str(output_directory / (name + '.v')),
            str(output_directory / "panda_libtech.v")
        ])

        return super().run(initial_state, skip=[bambu_step.id], **kwargs)
