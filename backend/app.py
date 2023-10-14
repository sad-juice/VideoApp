from flask import Flask, jsonify, request, abort
import json

def read(filename):
    with open(filename) as jsonfile:
        return json.load(jsonfile)

def write(data, filename):
    with open(filename, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

vidFile = "data/videos.json"
userFile = "data/users.json"
videos = read(vidFile)
users = read(userFile)

app = Flask(__name__)

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
    write(videos, vidFile)
    return new_video, 201

@app.route("/api/videos/<string:vid>", methods=['PUT'])
def update_video(vid):
    for video in videos:
        if video["vid"] == vid:
            video["title"] = request.json["title"]
            video["author"] = request.json["author"]
            video["views"] = request.json["views"]
            write(videos, vidFile)
            return video
    
    return jsonify({"error": "Video not found"}), 404

@app.route("/api/videos/<string:vid>", methods=['DELETE'])
def delete_video(vid):
    for video in videos:
        if video["vid"] == vid:
            videos.remove(video)
            write(videos, vidFile)
            return video
    
    return jsonify({"error": "Video not found"}), 404

@app.route("/api/users", methods=['GET'])
def get_users():
    return users

@app.route("/api/users/<string:name>", methods=['GET'])
def get_user(name):
    for user in users:
        if user["name"] == name:
            return user
        
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users", methods=['POST'])
def create_user():
    new_user = {
        "name": request.json["name"],
        "passwd": request.json["passwd"],
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
        if user["name"] == request.json["name"]:
            return jsonify({"error": "User already exists"}), 400
        
    users.append(new_user)
    write(users, userFile)
    return new_user, 201

@app.route("/api/users/<string:name>", methods=['DELETE'])
def delete_user(name):
    for user in users:
        if user["name"] == name:
            users.remove(user)
            write(users, userFile)
            return user
        
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users/<string:name>/levels", methods=['PUT'])
def update_user_levels(name):
    for user in users:
        if user["name"] == name:
            new_levels = {
                "serve": request.json["serve"],
                "forehand": request.json["forehand"],
                "backhand": request.json["backhand"],
                "forevolley": request.json["forevolley"],
                "backvolley": request.json["backvolley"],
                "overhead": request.json["overhead"]
            }
            user["levels"] = new_levels
            write(users, userFile)
            return new_levels
        
    return jsonify({"error": "User not found"}), 404        

if __name__ == '__main__':
    app.run(debug=True)