import pymongo
from hashlib import sha256

class MeetLangDatabase:
    host = 'mongodb+srv://userAdmin:passAdmin@cluster0.fl0ij.azure.mongodb.net/test?authSource=admin&' + \
    'replicaSet=atlas-nmj44l-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true'
    port = 27017
    client = pymongo.MongoClient(host, port)

class UsersDatabase(MeetLangDatabase):
    
    usersDatabase = MeetLangDatabase.client.UsersDatabase
    usersCollection = usersDatabase.Users
    usersTagsCollection = usersDatabase.UsersTags
    usersLanguagesCollection = usersDatabase.UsersLanguages
    
    @staticmethod
    def AddUser(user):
        UsersDatabase.usersCollection.insert_one(user).inserted_id
    @staticmethod
    def UpdateUserData(user, newData):
        UsersDatabase.usersCollection.update_one(user, newData)
    @staticmethod
    def UpdateUserTags(user, newTags):
        userTags = UsersDatabase.usersTagsCollection.find_one({"email":user['email']})
        UsersDatabase.usersTagsCollection.update_one(userTags, newTags)
    @staticmethod
    def UpdateUserLanguages(user, newLanguages):
        userLanguages = UsersDatabase.usersLanguagesCollection.find_one({"email":user['email']})
        UsersDatabase.usersTagsCollection.update_one(userLanguages, newLanguages)
    @staticmethod
    def RemoveUser(user):
        UsersDatabase.usersLanguagesCollection.delete_one(UsersDatabase.usersLanguagesCollection.find_one({"email":user['email']}))
        UsersDatabase.usersTagsCollection.delete_one(UsersDatabase.usersTagsCollection.find_one({"email":user['email']}))
        UsersDatabase.usersCollection.remove(user)
    @staticmethod
    def DoesUserExist(userEmail):
        if(UsersDatabase.usersCollection.find_one({"email":userEmail}) != None):
            return True
        else:
            return False
    @staticmethod
    def ReturnUserInfo(userEmail):
        userData ={}
        data = UsersDatabase.usersCollection.find_one({"email":userEmail})
        for key in data:
            if(key != "_id" and key != "password"):
                userData[key] = data[key]
        
        userTags = {}
        data = UsersDatabase.usersTagsCollection.find_one({{"email":userEmail}})
        for key in data:
            if(key != "_id" and key != "email"):
                userTags[key] = data[key]
        
        userLanguages = {}
        data = UsersDatabase.usersLanguagesCollection.find_one({{"email":userEmail}})
        for key in data:
            if(key != "_id" and key != "email"):
                userLanguages[key] = data[key]
        
        return {"user data":userData,"user tags":userTags, "user languages":userLanguages}
    @staticmethod
    def IsPasswordCorrect(userEmail, password):
        user = UsersDatabase.usersCollection.find_one({"email":userEmail})
        if(user['password'] == password):
            return True
        else:
            return False

class AccessTokensDatabase(MeetLangDatabase):
    accessTokensDatabase = MeetLangDatabase.client.AccessTokensDatabase
    activeTokens = accessTokensDatabase.ActiveTokens
    clients = accessTokensDatabase.Clients

    @staticmethod
    def RegisterNewClient(state):
        AccessTokensDatabase.clients.insert_one({"state":state})
        newClient = AccessTokensDatabase.clients.find_one({"state":state})
        AccessTokensDatabase.clients.update_one(newClient, {"$set":{"client_id":str(newClient['_id'])}})
        return str(newClient['_id'])
    @staticmethod
    def FindExistingClientByState(state):
        return AccessTokensDatabase.clients.find_one({"state":state})
    @staticmethod
    def FindExistingClientByClientId(clientId):
        return AccessTokensDatabase.clients.find_one({"client_id":clientId})
    @staticmethod
    def FindExistingClient(clientId, state):
        return AccessTokensDatabase.clients.find_one({"client_id":clientId, "state":state})
    @staticmethod
    def AddNewActiveToken(clientId, state, codeChallenge, scope):
        AccessTokensDatabase.activeTokens.insert_one({"client_id":clientId,"state":state})
        newToken = AccessTokensDatabase.activeTokens.find_one({"client_id":clientId,"state":state})

        code = str(newToken['_id'])
        AccessTokensDatabase.activeTokens.update_one(newToken, {"$set":{"code":code,"code_challenge":codeChallenge,"scope":scope}})
        return code
    @staticmethod
    def FindActiveToken(code):
        return AccessTokensDatabase.activeTokens.find_one({"code":code})
    @staticmethod
    def IsTokenValid(token):
        testedToken = AccessTokensDatabase.activeTokens.find_one({"client_id":token['client_id'],"state":token['state'],"code":token['code']})
        codeChallenge = testedToken['code_challenge']
        if(codeChallenge == sha256(bytes(token['code_verifier'], encoding='utf-8')).hexdigest() ):
            return True
        else:
            return False