# Test della pagina Home
def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Event Manager" in response.text

# Test dei file statici e del CSS
def test_static_files(client):
    response = client.get("/static/styles.css")
    assert response.status_code == 200