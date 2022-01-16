from email import header
import pytest
import bcrypt
import json
import config

from app import create_app
from sqlalchemy import create_engine, text

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow =0)

@pytest.fixture
def api():
  app = create_app(config.test_config)
  
  app.config['TEST'] = True
  api = app.test_client()

  return api
# 여기서 나는 어떻게 app.py랑 연결되었는지 궁금했는데, 위에서 출력했다. from app import create_app
# 그러면 create_app 밑에 있는 여러 end point함수들을 다 사용할 수 있다.
# 결국 중요한 것은 함수 이름이다, return 값 까지 함수 이름이랑 같을 필요는 없다.

def setup_function():
  hashed_password = bcrypt.hashpw(b'1234', bcrypt.gensalt())

  new_users = [
      {
      'id' : 1,
      'email' : 'jung123',
      'hashed_password' : hashed_password,
      'name' : 'JungHwanLee',
      'profile':'hola me llamo benuas'
      }, {
      'id' : 2,
      'email' : 'kkk123',
      'hashed_password' : hashed_password,
      'name' : 'kimjiju',
      'profile':'hola me llamo benuas'
      } 
  ]

  database.execute(text("""
    INSERT INTO users(
      id,
      name,
      email,
      profile,
      hashed_password
    ) VALUES (
      :id,
      :name,
      :email,
      :profile,
      :hashed_password
    )  
  """), new_users)

  database.execute(text("""
    INSERT INTO tweets (
      user_id,
      tweet
    ) VALUES (
      2,
      "second tweet"
    )
  """))

def teardown_function():
  database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
  database.execute(text("TRUNCATE users"))
  database.execute(text("TRUNCATE tweets"))
  database.execute(text("TRUNCATE users_follow_list"))
  database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_ping(api):
  resp = api.get('/ping')
  assert b'pong' in resp.data

def test_login(api):
  resp = api.post(
    '/login',
    data = json.dumps({ 'email':'jung123', 'password':'1234'}),
    content_type = 'application/json'
  )
  assert b"access_token" in resp.data

def test_unauthorized(api):
  resp = api.post(
    '/tweet',
    data = json.dumps({'tweet':'fitst tweet'}),
    content_type = 'application/json'
  )
  assert resp.status_code == 401

  resp = api.post(
    '/follow',
    data = json.dumps({'follow':2}),
    content_type = 'application/json'
  )
  assert resp.status_code == 401

  resp = api.post(
    '/unfollow',
    data = json.dumps({'unfollow':2}),
    content_type = 'application/json'
  )
  assert resp.status_code == 401

def test_tweet(api):
  resp = api.post(
    '/login',
    data = json.dumps({ 'email':'jung123', 'password':'1234'}),
    content_type = 'application/json'
  )

  resp_json = json.loads(resp.data.decode('utf-8'))
  access_token = resp_json['access_token']

  resp = api.post(
    '/tweet',
    data = json.dumps({'tweet':'first tweet'}),
    content_type = 'application/json',
    headers = {'Authorization': access_token}
  )
  assert resp.status_code == 200

  resp = api.get(f'/timeline/1')
  tweets = json.loads(resp.data.decode('utf-8'))
  assert resp.status_code == 200
  assert tweets == {
    'user_id': 1,
    'timeline':[
      {
        'user_id':1,
        'tweet':'first tweet'
      }
    ]
  }

def test_follow(api):
  resp = api.post(
    '/login',
    data = json.dumps({ 'email':'jung123', 'password':'1234'}),
    content_type = 'application/json'
  )
  resp_json = json.loads(resp.data.decode('utf-8'))
  access_token = resp_json['access_token']

  resp = api.get(f'/timeline/1')
  tweets = json.loads(resp.data.decode('utf-8'))
  assert resp.status_code == 200
  assert tweets == {
    'user_id' : 1,
    'timeline' : []
  }

  resp = api.post(
    '/follow',
    data = json.dumps({ 'follow' : 2}),
    content_type = 'application/json',
    headers = {'Authorization': access_token}
  )
  assert resp.status_code == 200

  resp = api.get(f'/timeline/1')
  tweets = json.loads(resp.data.decode('utf-8'))
  assert resp.status_code == 200
  assert tweets == {
    'user_id' : 1,
    'timeline' : [
      {
        'user_id' : 2,
        'tweet' : 'second tweet'
      }
    ]
  }

def test_unfollow(api):
  resp = api.post(
    '/login',
    data = json.dumps({ 'email':'jung123', 'password':'1234'}),
    content_type = 'application/json'
  )
  resp_json = json.loads(resp.data.decode('utf-8'))
  access_token = resp_json['access_token']

  resp = api.post(
    '/follow',
    data = json.dumps({ 'follow' : 2}),
    content_type = 'application/json',
    headers = {'Authorization': access_token}
  )
  assert resp.status_code == 200

  resp = api.get(f'/timeline/1')
  tweets = json.loads(resp.data.decode('utf-8'))
  assert resp.status_code == 200
  assert tweets == {
    'user_id' : 1,
    'timeline' : [
      {
        'user_id' : 2,
        'tweet' : 'second tweet'
      }
    ]
  }

  resp = api.post(
    '/unfollow',
    data = json.dumps({ 'unfollow' : 2}),
    content_type = 'application/json',
    headers = {'Authorization': access_token}
  )
  assert resp.status_code == 200

  resp = api.get(f'/timeline/1')
  tweets = json.loads(resp.data.decode('utf-8'))
  assert resp.status_code == 200
  assert tweets == {
    'user_id' : 1,
    'timeline' : []
  }