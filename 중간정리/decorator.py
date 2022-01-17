import jwt

from functools import wraps
from flask import request, Response

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    access_tocken = request.headers.get('Authorization')
    if access_tocken is not None:
      try:
        payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
      except jwt.InvalidTokenError:
        payload=None

      if payload is None: return Response(status=401)

      user_id = payload['user_id']
      g.user_id = user_id
      g.user = get_user_info(user_id) if user_id else None

    else:
      return Response(status = 401)

    return f(*args, **kwargs)
  return decorated_function