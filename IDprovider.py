from MeetLangClasses.MeetLangDatabaseFile import UsersDatabase, AccessTokensDatabase
from MeetLangClasses.CommunicationStatus import CommunicationStatus
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/Register', methods = ['POST'])
def Register():
    data = request.json
    clientId = AccessTokensDatabase.RegisterNewClient(data['state'])
    return CommunicationStatus.Success({"client_id":clientId})

@app.route('/Authorize', methods = ['GET'])
def Authorize():
    clientId = request.args.get('client_id')
    state = request.args.get('state')
    if(AccessTokensDatabase.FindExistingClient(clientId, state) != None):
        codeChallenge = request.args.get('code_challenge')
        scope = request.args.get('scope')

        code = AccessTokensDatabase.AddNewActiveToken(clientId, state, codeChallenge, scope)

        return CommunicationStatus.Success({"code":code})
    else:
        return CommunicationStatus.UnregisteredClient()

@app.route('/Token', methods = ['POST'])
def Token():
    data = request.json
    token = data['header']
    if(AccessTokensDatabase.FindExistingClient(token['client_id'], token['state']) == None):
        return CommunicationStatus.UnregisteredClient()
    elif(AccessTokensDatabase.FindActiveToken(token['code']) == None):
        return CommunicationStatus.InactiveToken()
    elif(AccessTokensDatabase.IsTokenValid(token)):
        requestType = data['request']
        if(requestType['type'] == "login"):
            if(UsersDatabase.DoesUserExist(token['scope']) == False):
                return CommunicationStatus.NonExistingUser()
            elif(UsersDatabase.IsPasswordCorrect(token['scope'], requestType['password']) == False):
                return CommunicationStatus.WrongPassword()
            else:
                return CommunicationStatus.Success(UsersDatabase.ReturnUserInfo(token['scope']))
        else:
            return CommunicationStatus.UndefinedFail()
    else:
        return CommunicationStatus.InactiveToken()


#heroku implementation requirement
if (__name__ == "__main__"):
    app.run()