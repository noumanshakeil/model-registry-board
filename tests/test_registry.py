import pytest

@pytest.mark.asyncio
async def test_promote_flow(client):
    c = await client.post("/api/cards", json={"name": "churn-rf", "description": "baseline"})
    cid = c.json()["id"]
    v = await client.post(f"/api/cards/{cid}/versions", json={"version": "1.0.0", "artifact_uri": "s3://x"})
    vid = v.json()["id"]
    assert v.json()["stage"] == "staging"
    p = await client.post(f"/api/versions/{vid}/promote")
    assert p.json()["stage"] == "prod"
    d = await client.post(f"/api/versions/{vid}/demote")
    assert d.json()["stage"] == "staging"
