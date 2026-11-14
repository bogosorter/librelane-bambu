from librelane.flows import Flow
from custom_flow import CustomFlow

flow = CustomFlow("config.json", pdk="sky130A", pdk_root="/home/bogosorter/.ciel/ciel/sky130/versions/8afc8346a57fe1ab7934ba5a6056ea8b43078e71")
flow.start()
