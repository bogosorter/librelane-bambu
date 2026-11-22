# LibreLane Plugin for Bambu

This plugin augments LibreLane with a step from C to Verilog, as well as a flow that extends the classic flow with this step.

## Installing

Please [install LibreLane](https://librelane.readthedocs.io/en/stable/installation/index.html) and [download the latest Bambu AppImage](https://release.bambuhls.eu/). Additionally, the environment should contain a variable `BAMBU_PATH` that points to the Bambu binary. If, for instance, the binary is under `/home/bogosorter/bin/bambu-2026.11.AppImage`, you might add this line to your `~/.bashrc`:

```
export BAMBU_PATH="/home/bogosorter/bin/bambu-2026.11.AppImage"
```

The next step is to clone this repository. If all steps were executed correctly, the only thing missing is to add the cloned repository's path to the `PYTHONPATH` environment variable. *From the nix shell created by LibreLane*, you can simply source the provided `env.sh`:

```
git clone git@github.com:bogosorter/librelane-bambu.git
cd librelane-bambu
source env.sh
```

To run a quick check, you can try to run the example:

```
librelane example/config.json --flow BambuFlow
```

## Usage

This plugin integrates naturally into LibreLane. The step and the flow are registered in the LibreLane registry, and you can use them through the command line or through a script. As usual in LibreLane, the entry for compilation is `config.json`. Instead of supplying the `VERILOG_FILES` variable, you should now set only the `C_FILE` variable.
