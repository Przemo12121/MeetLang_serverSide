import json
from flask import Flask, request
import pymongo
from hashlib import sha256
from PythonMongoDBmenagement.PythonMongoDBmenagement import UsersDatabase

class AccessTokensDatabase:
    host = 'mongodb+srv://userAdmin:passAdmin@cluster0.fl0ij.azure.mongodb.net/test?authSource=admin&' + \
    'replicaSet=atlas-nmj44l-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true'
    port = 27017
    client = pymongo.MongoClient(host, port)
    tokens_database = client.AccessTokensDatabase
    active_tokens = tokens_database.ActiveTokens
    clients = tokens_database.Clients

    @staticmethod
    def AddNewToken(token):
        AccessTokensDatabase.active_tokens.insert_one(token).inserted_id
    @staticmethod
    def RegisterNewClient():
        client_id = "qwerty"
        state = "abc"
        if(AccessTokensDatabase.FindExistingClient({"client_id":client_id, "state":state}) == None):
            AccessTokensDatabase.clients.insert_one({"client_id":client_id, "state":state}).inserted_id
        return client_id
    @staticmethod
    def FindExistingClient(data):
        return AccessTokensDatabase.clients.find_one({"client_id":data['client_id'], "state":data['state']})
    @staticmethod
    def ReturnAccessToken(token):
        token_info = {}
        for key in token:
            if(key != "_id" and key != "code_challenge" and key != "client_id" and key != "state"):
                token_info[key] = token[key]
        return token_info
    @staticmethod
    def GenerateCode():
        return "testCode"
    @staticmethod
    def FindMatchingAccessToken(token):
        return AccessTokensDatabase.active_tokens.find_one({"code":token['code']})
    @staticmethod
    def IsPostedTokenValid(token):  #validation not working
        code_challenge = sha256(bytes(token['code_verifier'], encoding='utf-8')).hexdigest()
        if(code_challenge == AccessTokensDatabase.FindMatchingAccessToken(token)['code_challenge']):
            return True
        else:
            return False

app = Flask(__name__)

#AccessTokensDatabase.RegisterNewClient()

@app.route('/Authorize', methods = ['GET'])
def Authorize():
    client_id = request.args.get('client_id')
    state = request.args.get('state')
    if(AccessTokensDatabase.FindExistingClient({"client_id":client_id,"state":state}) != None):
        code_challenge = request.args.get('code_challenge')
        scope = request.args.get('scope')

        new_token = {"client_id":client_id,"state":state,
            "scope":scope,
            "code_challenge":code_challenge, "code":AccessTokensDatabase.GenerateCode()}
        
        AccessTokensDatabase.AddNewToken(new_token)

        return AccessTokensDatabase.ReturnAccessToken(new_token)
    else:
        return {"status":"Client is not registered."}

@app.route('/Token', methods = ['POST'])
def Token():
    data = request.json
    token = data['header']
    if(AccessTokensDatabase.FindExistingClient(token) == None):
        return {"status":"Client not registered."}
    elif(AccessTokensDatabase.FindMatchingAccessToken(token) == None):
        return {"status":"Posted token is inactive."}
    elif(AccessTokensDatabase.IsPostedTokenValid(token)):
        requestType = data['request']
        if(requestType['type'] == "login"):
            user = UsersDatabase.get_existing_user({"email":token['scope']})
            if(user == None):
                return {"status":"user not found"}
            elif(requestType['password'] == user['password']):
                return UsersDatabase.return_user_info(user)
            else:
                return {"status":"invalid password"}
        else:
            return {"status":"request not yet accessible"}
    else:
        return {"status":"Posted token is invalid."}

app.run(port=5000)