import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
APPLICATION = ROOT / "src" / "MS_Teams_Busy_Light.py"


def load_application(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_incoming_call_uses_supported_blink_command(monkeypatch):
    application = load_application(APPLICATION, "ms_teams_busy_light")
    writes = []

    if hasattr(application, "send_to_busy_light"):
        monkeypatch.setattr(application, "send_to_busy_light", writes.append)
    else:
        class FakeSerial:
            def write(self, command):
                writes.append(command)

            def flush(self):
                pass

        monkeypatch.setattr(application, "ser", FakeSerial())
        monkeypatch.setattr(application.time, "sleep", lambda _seconds: None)

    application.write_status_to_busy_light("incomingcall")

    assert writes == [b"BlinkRed\r\n"]


def test_legacy_teams_configuration_is_rejected(tmp_path):
    application = load_application(APPLICATION, "ms_teams_busy_light")
    config_file = tmp_path / "settings.ini"
    config_file.write_text("[Version]\nnewTeams = False\n", encoding="utf-8")

    assert application.load_settings(config_file) is None
