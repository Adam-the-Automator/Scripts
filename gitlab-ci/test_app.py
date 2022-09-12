from app import app

def test_main():
		# Creates a test client for this application.
    response = app.test_client().get('/') 

		# assert the stutus code of the page('/') is 200
    assert response.status_code == 200 
		# assert the return statement to the page
    assert response.data == b'Hello World!'
