def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_status_requires_key(client):
    assert client.get("/v1/status").status_code == 401

def test_project_create_and_list(client, auth_headers):
    payload = {"name":"Sample Project","description":"Project details","technologies":["Python"],"facts":{"metric":"verified"}}
    created = client.post("/v1/projects", json=payload, headers=auth_headers)
    assert created.status_code == 200 and created.json()["name"] == "Sample Project"
    assert any(x["name"] == "Sample Project" for x in client.get("/v1/projects", headers=auth_headers).json())

def test_profile_upsert(client, auth_headers):
    r = client.put("/v1/profile", json={"full_name":"Test Person","email":"test@example.com"}, headers=auth_headers)
    assert r.status_code == 200 and r.json()["full_name"] == "Test Person"

def test_n8n_requires_token(client):
    assert client.post("/v1/n8n/scan-start").status_code == 401

def test_n8n_queues_approval(client):
    r = client.post("/v1/n8n/scan-start", headers={"X-N8N-Token":"test-n8n-token"})
    assert r.status_code == 200 and r.json()["status"] == "pending_approval"
