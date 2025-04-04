import json
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
{"name": "Sm9obiBEb2U=","age": "MzA=","contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5j..."}
@pytest.mark.parametrize("payload, encrypted", (
        pytest.param("null", '"bnVsbA=="', id="null_payload"),
        pytest.param("[]", '[]', id="empty_list"),
        pytest.param("1", '"MQ=="', id="number"),
        pytest.param('"123"', '"IjEyMyI="', id="string"),
        pytest.param('123', '"MTIz"', id="number"),
        pytest.param('[1, null, {}, {"a": 7}]', '["MQ==", "bnVsbA==", "e30=", "eyJhIjogN30="]', id="non_empty_list"),
        pytest.param('{}', '{}', id="empty_object"),
        pytest.param("[1, 2, 3]", '["MQ==", "Mg==", "Mw=="]', id="list_of_ints"),
        pytest.param('[1, {}, "abs", [], [1, {}]]', '["MQ==", "e30=", "ImFicyI=", "W10=", "WzEsIHt9XQ=="]', id="list_of_misc"),
        pytest.param('{"z": 3, "a": 1, "c": 53}', '{"a": "MQ==", "z": "Mw==", "c": "NTM="}', id="object_of_ints"),
        pytest.param('{"a": 3, "b": {"c": "v"}}', '{"a":"Mw==","b":"eyJjIjogInYifQ=="}', id="object_misc"),
        pytest.param('{"z": 3, "a": {"a.b": [1, 2, 3, 4], "a.c": null}, "c": 53}', '{"a": "eyJhLmIiOiBbMSwgMiwgMywgNF0sICJhLmMiOiBudWxsfQ==", "z": "Mw==", "c": "NTM="}', id="nested_objects"),
        pytest.param('{"name": "John Doe", "age": 30,"contact": {"email": "john@example.com","phone": "123-456-7890"}}', '{"name": "IkpvaG4gRG9lIg==","age": "MzA=","contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9"}', id="example_1"),
        pytest.param('{"name": "John Doe", "age": 30,"contact": {"email": "john@example.com","phone": "123-456-7890"}}', '{"name": "Sm9obiBEb2U=","age": "MzA=","contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9"}', id="example_1", marks=pytest.mark.xfail),
))
def test_cypher(payload, encrypted):
    # Encrypting
    response = client.post("/encrypt", content=payload)
    assert response.status_code == 200
    assert response.json() == json.loads(encrypted)

    # Decrypting
    response = client.post("/decrypt", content=encrypted)
    assert response.status_code == 200
    assert response.json() == json.loads(payload)


@pytest.mark.parametrize("payload, decrypted", (
        pytest.param("[1, 2, 3]", "[1, 2, 3]", id="uncrypted_list"),
        pytest.param('{"z": 3, "a": 1, "c": 53}', '{"a": 1, "z": 3, "c": 53}', id="uncrypted_object"),
        pytest.param('{"z": 3, "a": {"a.b": [1, 2, 3, 4], "a.c": null}, "c": 53}', '{"z": 3, "a": {"a.b": [1, 2, 3, 4], "a.c": null}, "c": 53}', id="uncrypted_nested_object"),
        pytest.param('{"z": 3, "c": "NTM=", "a": {"a.b": [1, 2, 3, 4], "a.c": null}}', '{"a": {"a.c": null, "a.b": [1, 2, 3, 4]}, "c": 53, "z": 3}', id="partly_crypted_object"),
        pytest.param('"MTIz"', '123', id="casting_order"),
))
def test_decrypt_advanced(payload, decrypted):
    decrypted_response = client.post("/decrypt", content=payload)
    assert decrypted_response.status_code == 200
    assert decrypted_response.json() == json.loads(decrypted)

# b64decode(data).decode() works
# string 123

@pytest.mark.parametrize("payload",(
        pytest.param('', id="empty_payload"),
))
def test_cypher_errors(payload):
    response = client.post("/encrypt", content=payload)
    assert response.status_code == 400
    assert not response.content

    response = client.post("/decrypt", content=payload)
    assert response.status_code == 400
    assert not response.content
