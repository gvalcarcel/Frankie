from __future__ import annotations

from frankie.live.engine import run_live_command
from frankie.live.renderer import render_live_json, render_live_text


def dispatch(command_type: str, simulated: bool = False, json_output: bool = False) -> str:
    result = run_live_command(command_type, simulated=simulated)
    return render_live_json(result) if json_output else render_live_text(result)
