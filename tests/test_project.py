from django.core.management import call_command


def test_system_check_passes():
    call_command("check", fail_level="WARNING")
