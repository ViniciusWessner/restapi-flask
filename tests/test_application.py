import pytest
from application import create_app

class TestApplication():
  
    @pytest.fixture  
    def client(self):
      app = create_app('config.MockConfig')
      return app.test_client()
    
    @pytest.fixture
    def valid_user(self):
        return {
          "cpf":"873.800.650-25",
          "first_name": "Vinicius",
          "last_name": "Wessner",
          "email": "vinmi@gmail.com",
          "birth_Date": "1997-05-31"
        }
    
    @pytest.fixture
    def invalid_user(self):
        return {
          "cpf":"873.800.650-29",
          "first_name": "Vinicius",
          "last_name": "Wessner",
          "email": "vinmi@gmail.com",
          "birth_Date": "1997-05-31"
        }
    
    def test_get_users(self, client):
      response = client.get('/users')
      assert response.status_code == 200
      
    def test_post_user(self, client, valid_user, invalid_user):
      response = client.post('/user', json=valid_user)
      assert response.status_code==200
      assert b"sucesso" in response.data
      
      response = client.post('/user', json=invalid_user)
      assert response.status_code==400
      assert b"invalido" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
      response = client.get('/user/%s' %valid_user["cpf"])
      assert response.status_code == 200
      assert response.json[0]["first_name"] == "Vinicius"
      assert response.json[0]["last_name"] == "Wessner"
      assert response.json[0]["email"] == "vinmi@gmail.com"
      assert response.json[0]["cpf"] == "873.800.650-25"
      
      
      response = client.get('/user/%s' %invalid_user["cpf"])
      assert response.status_code == 400
      assert b"Usuario nao encontrado" in response.data
