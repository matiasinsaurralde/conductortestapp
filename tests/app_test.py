from project.app import create_app
app = create_app()

def test_healthz():
    tester = app.test_client()
    response = tester.get("/healthz", content_type="html/text")
    assert response.status_code == 402

def test_get_user():
    tester = app.test_client()
    response = tester.get("/v1/user", content_type="application/json", headers={
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1NTQ3NTU1NTUsImV4cCI6MjU1NDc1NTUwMCwiaWF0IjoxNTU0NzU1NTAwLCJqdGkiOiI5ZmRmMGE2Ni00YzllLTRlOTktODc4MC05YjdlOTNlMjFlMjciLCJ1c2VyX2lkIjoiMTA1YjM1MTgtNjQ2ZC00NjNlLWFkZGEtZDJiOTM5YzJkMDZkIiwidXNlcl9mdWxsX25hbWUiOiJCZXJ0cmFtIEdpbGZveWxlIiwidXNlcl9lbWFpbCI6Im51bGxAcGllZHBpcGVyLmNvbSJ9.-A8Gx18iTikKpedcxDlgcc7D8GMWFix0709Vfpbo1SI'
    })
    assert response.status_code == 200

def test_get_user_forbidden():
    tester = app.test_client()
    response = tester.get("/v1/user", content_type="application/json")
    assert response.status_code == 403