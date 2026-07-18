from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_inspection_type():

    response = client.post(
        "/inspections/types",
        json={
            "title": "بازرسی مراکز عرضه",
            "description": "بازرسی بهداشتی مراکز عرضه مواد غذایی",
            "is_active": True
        }
    )

    assert response.status_code in [
        200,
        201
    ]


def test_get_inspection_types():

    response = client.get(
        "/inspections/types"
    )

    assert response.status_code == 200