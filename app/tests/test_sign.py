import json
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("payload", (
        pytest.param("null", id="null_payload"),
        pytest.param("[]", id="empty_list"),
        pytest.param("1", id="number"),
        pytest.param('"123"', id="string"),
        pytest.param('[1, null, {}, {"a": 7}]', id="non_empty_list"),
        pytest.param('{}', id="empty_object"),
        pytest.param('{"a": 3, "b": {"c": "v"}}', id="object_1"),
))
def test_sign(payload):
    # Signing
    response = client.post("/sign", content=payload)
    assert response.status_code == 200
    data = response.json()
    assert tuple(data.keys()) == ('signature',)

    # Verifying
    response = client.post("/verify", json={"data": json.loads(payload), **data})
    assert response.status_code == 204
    assert not response.content


@pytest.mark.parametrize("payload, verify_payload, status_code", (
        pytest.param("[1, 2, 3]", "[3, 1, 2]", 400, id="disordered_list"),
        pytest.param('{"z": 3, "a": 1, "c": 53}', '{"a": 1, "z": 3, "c": 53}', 204, id="reordered_object"),
        pytest.param('{"z": 3, "a": {"a.b": [1, 2, 3, 4], "a.c": null}, "c": 53}', '{"a": 1, "z": 3, "c": 53}', 400, id="diff_nested_object"),
        pytest.param('{"z": 3, "c": 53, "a": {"a.b": [1, 2, 3, 4], "a.c": null}}', '{"a": {"a.c": null, "a.b": [1, 2, 3, 4]}, "c": 53, "z": 3}', 204, id="same_nested_object"),
))
def test_sign_advanced(payload, verify_payload, status_code):
    # Signing
    sign_response = client.post("/sign", content=payload)
    assert sign_response.status_code == 200

    # Verifying
    response = client.post("/verify", json={"data": json.loads(verify_payload), **sign_response.json()})
    assert response.status_code == status_code
    assert not response.content

@pytest.mark.parametrize("payload",(
        pytest.param('', id="empty_payload"),
        pytest.param('1', id="wrong_payload_type"),
        pytest.param('{"content": "test"}', id="wrong_payload_content"),
        pytest.param('{"data": "test"}', id="no_signature"),
        pytest.param('{"content": "test", "signature": 1}', id="no_data"),
        pytest.param('{"data": "test", "signature": 1}', id="wrong_signature_type"),
        pytest.param('{"data": "test", "signature": "a43b"}', id="wrong_signature"),
        pytest.param('{"data": "test", "signature": "a43rt"}', id="wrong_signature_base64"),
))
def test_sign_errors(payload):
    response = client.post("/verify", content=payload)
    assert response.status_code == 400
    assert not response.content
