from flask import Flask, request, jsonify, abort
import jwt, re, os

app = Flask(__name__)

@app.get("/v1/user")
def get_user():
  res = {
    'user_id': request.decoded_jwt['user_id'],
    'user_full_name': request.decoded_jwt['user_full_name'],
    'user_email': request.decoded_jwt['user_email'],
  }
  return jsonify(res)

@app.get("/healthz")
def healthz():
  return "", 402

@app.before_request
def auth():
  # If path is healthz, skip the auth logic:
  if request.path == '/healthz':
    return
  # For other paths, return 403 if no auth header is set:
  if 'Authorization' not in request.headers:
    abort(403)
  auth_header_value = request.headers["Authorization"]
  # Extract the bearer token:
  matches = re.match("^Bearer\s+(.*)", auth_header_value)
  if not matches:
    abort(403)
  encoded_jwt = matches[1]
  try:
    # Decode JWT token using APP_JWT_SECRET:
    decoded_jwt = jwt.decode(encoded_jwt, os.getenv("APP_JWT_SECRET"), algorithms=["HS256"])
    # If the JWT token was successfully decoded, add it to the request object:
    request.decoded_jwt = decoded_jwt
  except:
    abort(403)
