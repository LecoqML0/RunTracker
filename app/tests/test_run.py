import uuid

from app.tests.conftest import client
from app.tests.helpers import register_user, login_user


def create_run(client, token, run_name, distance):
    return client.post(
        "/run/",
        json={"run_name": run_name, "distance": distance},
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_run_and_get_it(client):
    email = f"runuser_{uuid.uuid4().hex[:8]}@example.com"
    register_user(client, "runuser", email, "securepassword")
    token = login_user(client, email, "securepassword")

    response = create_run(client, token, "Morning Run", 5.2)
    assert response.status_code == 200
    payload = response.json()
    assert payload["run_name"] == "Morning Run"
    assert payload["distance"] == 5.2
    assert payload["user_id"] is not None
    assert payload["run_id"] is not None

    run_id = payload["run_id"]
    get_response = client.get(
        f"/run/{run_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 200
    assert get_response.json()["run_id"] == run_id
    assert get_response.json()["run_name"] == "Morning Run"


def test_list_runs_returns_user_runs(client):
    email = f"runlist_{uuid.uuid4().hex[:8]}@example.com"
    register_user(client, "runlistuser", email, "securepassword")
    token = login_user(client, email, "securepassword")

    create_run(client, token, "Run A", 3.1)
    create_run(client, token, "Run B", 7.5)

    response = client.get(
        "/run/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    runs = response.json()
    assert isinstance(runs, list)
    assert len(runs) >= 2
    names = {run["run_name"] for run in runs}
    assert {"Run A", "Run B"}.issubset(names)


def test_delete_run_removes_it(client):
    email = f"rundel_{uuid.uuid4().hex[:8]}@example.com"
    register_user(client, "rundeluser", email, "securepassword")
    token = login_user(client, email, "securepassword")

    response = create_run(client, token, "Temporary Run", 4.0)
    assert response.status_code == 200
    run_id = response.json()["run_id"]

    delete_response = client.delete(
        f"/run/{run_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["run_id"] == run_id

    get_response = client.get(
        f"/run/{run_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 404


def test_create_run_invalid_distance_returns_422(client):
    email = f"runinvalid_{uuid.uuid4().hex[:8]}@example.com"
    register_user(client, "runinvaliduser", email, "securepassword")
    token = login_user(client, email, "securepassword")

    response = create_run(client, token, "Bad Run", 0)
    assert response.status_code == 422
