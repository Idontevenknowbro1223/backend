import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "15C11E"
secretkey = "UMNH1IISP6OTNG63CWESQXSG9TBEHE9WTOIFQARQHXR63KPYF8"
applab = "OC|30104788022470243|9b5f59730c55096c12bc926afb87a604"

playfab_cache = {}

def auth():
    return {"content-type": "application/json", "X-SecretKey": secretkey}

@app.route("/api/PlayFabAuthentication", methods=["POST"])
def Idontknowwhattonamethislol():
    getjson = request.get_json()
    required_fields = ["CustomId", "Nonce", "AppId", "Platform", "OculusId"]
    missing_fields = [field for field in required_fields if not getjson.get(field)]
    
    if missing_fields:
        return jsonify({"Message": "error!", "Error": "no"}), 400
    
    if getjson.get("AppId") != title:
        return jsonify({"Message": "skkod", "Error": "skid??"}), 400
    
    if not getjson.get("CustomId").startswith("OCULUS"):
        return jsonify({"Message": "scary hacker!!", "Error": "ahcker"}), 400
    
    if not getjson.get("Platform").startswith("Quest"):
        return jsonify({"Message": "scary hacker!!", "Error": "ahcker"}), 400
    
    url = f"https://{title}.playfabapi.com/Server/LoginWithServerCustomId"
    login_request = requests.post(
        url=url,
        json={"ServerCustomId": getjson.get("CustomId"), "CreateAccount": True},
        headers=auth()
    )
    
    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")
        playfab_id = data.get("PlayFabId")
        
        url = f"https://{title}.playfabapi.com/Server/LinkServerCustomId"
        link_request = requests.post(
            url=url,
            json={"ForceLink": True, "PlayFabId": playfab_id, "ServerCustomId": getjson.get("CustomId")},
            headers=auth()
        )
        
        if link_request.status_code == 200:
            return jsonify({
                "PlayFabId": playfab_id,
                "SessionTicket": session_ticket,
                "EntityToken": entity_type,
                "EntityId": entity_id,
                "EntityType": entity_type
            }), 200
        else:
            return jsonify({"Message": "Link failed!", "Error": "failed"}), 400
    else:
        return jsonify({"Message": "Login failed!", "Error": "failed"}), 400

@app.route("/api/CachePlayFabId", methods=["POST"])
def somethingelsetodolol():
    getjson = request.get_json()
    playfab_cache[getjson.get("PlayFabId")] = getjson
    return jsonify({"Message": "Success"}), 200

@app.route("/api/TitleData", methods=["POST", "GET"])
def title_data():
    response = requests.post(url=f"https://{title}.playfabapi.com/Server/GetTitleData", headers=auth())
    if response.status_code == 200:
        return jsonify(response.json().get("data").get("Data"))
    else:
        return jsonify({}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
