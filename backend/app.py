from flask import Flask, jsonify, request, abort
import json

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, current_user
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

def read_json_file(filename):
    with open(filename) as jsonfile:
        return json.load(jsonfile)

def write_json_file(data, filename):
    with open(filename, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

videosFile = "data/videos.json"
usersFile = "data/users.json"
videos = read_json_file(videosFile)
users = read_json_file(usersFile)

load_dotenv()
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.logger.info("secret: ", app.config["JWT_SECRET_KEY"])
jwt = JWTManager(app)

########################
# API for Videos
########################
@app.route("/api/videos", methods=['GET'])
def get_videos():
    return videos

@app.route("/api/videos/<string:vid>", methods=['GET'])
def get_video(vid):
    for video in videos:
        if video["vid"] == vid:
            return video
    
    return jsonify({"error": "Video not found"}), 404

@app.route("/api/videos", methods=['POST'])
def create_video():
    new_video = {
        "vid": request.json["vid"],
        "title": request.json["title"],
        "author": request.json["author"],
        "views": request.json["views"]
    }

    for video in videos:
        if video["vid"] == request.json["vid"]:
            return jsonify({"error": "Video already exists"}), 400

    videos.append(new_video)
    write_json_file(videos, videosFile)
    return new_video, 201

@app.route("/api/videos/<string:vid>", methods=['PUT'])
def update_video(vid):
    for video in videos:
        if video["vid"] == vid:
            video["title"] = request.json["title"]
            video["author"] = request.json["author"]
            video["views"] = request.json["views"]
            write_json_file(videos, videosFile)
            return video
    
    return jsonify({"error": "Video not found"}), 404

@app.route("/api/videos/<string:vid>", methods=['DELETE'])
def delete_video(vid):
    for video in videos:
        if video["vid"] == vid:
            videos.remove(video)
            write_json_file(videos, videosFile)
            return video
    
    return jsonify({"error": "Video not found"}), 404

##############################
# API for Users and Levels
##############################
@app.route("/api/users", methods=['GET'])
def get_users():
    return users

@app.route("/api/users/<string:name>", methods=['GET'])
def get_user(name):
    for user in users:
        if user["username"] == name:
            return user
        
    return jsonify({"error": "User not found"}), 404

# @app.route("/api/users", methods=['POST'])
# def create_user():
#     new_user = {
#         "username": request.json["username"],
#         "password": request.json["password"],
#         "admin": False,
#         "levels": {
#             "serve": 0,
#             "forehand": 0,
#             "backhand": 0,
#             "forevolley": 0,
#             "backvolley": 0,
#             "overhead": 0
#         }
#     }

#     for user in users:
#         if user["username"] == request.json["username"]:
#             return jsonify({"error": "User already exists"}), 400
        
#     users.append(new_user)
#     write_json_file(users, usersFile)
#     return new_user, 201

@app.route("/api/users/<string:name>", methods=['DELETE'])
def delete_user(name):
    for user in users:
        if user["username"] == name:
            users.remove(user)
            write_json_file(users, usersFile)
            return user
        
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users/<string:name>/levels", methods=['PUT'])
def update_user_levels(name):
    for user in users:
        if user["username"] == name:
            new_levels = {
                "serve": request.json["serve"],
                "forehand": request.json["forehand"],
                "backhand": request.json["backhand"],
                "forevolley": request.json["forevolley"],
                "backvolley": request.json["backvolley"],
                "overhead": request.json["overhead"]
            }
            user["levels"] = new_levels
            write_json_file(users, usersFile)
            return new_levels
        
    return jsonify({"error": "User not found"}), 404        

##############################
# API for Signup and Login
##############################
@jwt.user_identity_loader
def user_identity_lookup(user):
  app.logger.info(f"lookup: user {user}")
  return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return identity

@app.route("/api/login", methods=["POST"])
def login():
  username = request.json.get("username", None)
  password = request.json.get("password", None)
  if (username and password):
    for user in users:
      if user["username"] == username and user["password"] == password:
        app.logger.info(f"user '{username}' login")
        additional_claims = {"admin": False}
        access_token = create_access_token(username, additional_claims=additional_claims)
        return jsonify({
        "username": username,
        "admin": user["admin"],
        "token": access_token,
        })

  app.logger.error(f"user '{username}' bad login")
  return jsonify({ "error": "invalid user and password" }), 401

@app.route("/api/signup", methods=["POST"])
def signup():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if (not username or not password):
      return jsonify({"error": "Username and password can't be empty"}), 400

    new_user = {
        "username": username,
        "password": password,
        "admin": False,
        "levels": {
            "serve": 0,
            "forehand": 0,
            "backhand": 0,
            "forevolley": 0,
            "backvolley": 0,
            "overhead": 0
        }
    }

    for user in users:
        if user["username"] == request.json["username"]:
            return jsonify({"error": "User already exists"}), 400
        
    users.append(new_user)
    write_json_file(users, usersFile)
    app.logger.info(f"user '{username}' was created")
    additional_claims = {"admin": False}
    access_token = create_access_token(username, additional_claims=additional_claims)
    return jsonify({
        "username": username,
        "admin": new_user["admin"],
        "token": access_token,
        })

@app.route("/api/whoami", methods=['GET'])
@jwt_required()
def whoami():
  username = f"{current_user}"
  data = None
  for user in users:
    if user["username"] == username:
      data = user
      break
    
  if (data) :
    return jsonify({"message": f"Hello {username}"}), 200
  else:
    return jsonify({"message": f"User {username} not found"}), 401

@app.route("/api/adminwhoami", methods=['GET'])
@jwt_required()
def admin_whoami():
  username = f"{current_user}"
  data = None
  for user in users:
    if user["username"] == username:
      data = user
      break

  if (user["admin"]):
    return jsonify({"message": f"Hello {username}"}), 200
  else:
    return jsonify({"message": f"User {username} do not have permission for this API."}), 403

if __name__ == '__main__':
  app.run(debug=True)