def test_wallet_info_integration(client, monkeypatch, dummy_get_account_info):
    monkeypatch.setattr("app.services.tron_service.TronService.get_account_info", dummy_get_account_info)
    payload = {"address": "TYav58BSjcRnUmvJkDLX365kGms2q9q6wZ"}
    response = client.post("/wallet_info", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "TYav58BSjcRnUmvJkDLX365kGms2q9q6wZ"
    assert data["balance"] == 12345678
    assert data["bandwidth"] == 800
    assert data["energy"] == 400
