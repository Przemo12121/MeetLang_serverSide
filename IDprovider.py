from MeetLangClasses.MeetLangDatabaseFile import UsersDatabase, AccessTokensDatabase
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/Register', methods = ['POST'])
def Register():
    data = request.json
    clientId = AccessTokensDatabase.RegisterNewClient(data['state'])
    return {"client_id":clientId}

@app.route('/Authorize', methods = ['GET'])
def Authorize():
    clientId = request.args.get('client_id')
    state = request.args.get('state')
    if(AccessTokensDatabase.FindExistingClient(clientId, state) != None):
        codeChallenge = request.args.get('code_challenge')
        scope = request.args.get('scope')

        code = AccessTokensDatabase.AddNewActiveToken(clientId, state, codeChallenge, scope)

        return {"code":code}
    else:
        return {"status":"Client is not registered."}

@app.route('/Token', methods = ['POST'])
def Token():
    data = request.json
    token = data['header']
    if(AccessTokensDatabase.FindExistingClient(token['client_id'], token['state']) == None):
        return {"status":"Client not registered."}
    elif(AccessTokensDatabase.FindActiveToken(token['code']) == None):
         return {"status":"Posted token is inactive."}
    elif(AccessTokensDatabase.IsTokenValid(token)):
        requestType = data['request']
        if(requestType['type'] == "login"):
            if(UsersDatabase.DoesUserExist(token['scope']) == False):
                return {"status":"user not found"}
            elif(UsersDatabase.IsPasswordCorrect(token['scope'], requestType['password']) == False):
                return {"status":"invalid password"}
            else:
                return UsersDatabase.ReturnUserInfo(token['scope'])
        else:
            return {"status":"request not yet accessible"}
    else:
        return {"status":"Posted token is invalid."}


#heroku implementation requirement
if (__name__ == "__main__"):
    app.run()