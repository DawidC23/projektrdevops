from src.health_logic import app_status

def test_app_logic():
    result = app_status()
    assert result["status"] == "ok"
