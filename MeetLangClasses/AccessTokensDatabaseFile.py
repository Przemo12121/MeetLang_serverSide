from MeetLangDatabaseFile import MeetLangDatabase

class AccessTokensDatabase(MeetLangDatabase):
    
    accessTokensDatabase = MeetLangDatabase.client.AccessTokensDatabase
    activeTokens = accessTokensDatabase.ActiveTokens
    clients = accessTokensDatabase.Clients

    @staticmethod
    def RegisterNewClient(state):
        AccessTokensDatabase.clients.insert_one({"state":state})
        newClient = AccessTokensDatabase.clients.find_one({"state":state})
        AccessTokensDatabase.clients.update_one(newClient, {"$set":{"client_id":str(newClient['_id'])}})
    @staticmethod
    def FindExistingClientByState(state):
        return AccessTokensDatabase.clients.find_one({"state":state})
    @staticmethod
    def FindExistingClientByClientId(clientId):
        return AccessTokensDatabase.clients.find_one({"client_id":clientId})
    @staticmethod
    def AddNewActiveToken(clientId, state, codeChallenge, scope):
        AccessTokensDatabase.activeTokens.insert_one({"client_id":clientId,"state":state})
        newToken = AccessTokensDatabase.activeTokens.find_one({"client_id":clientId,"state":state})

        code = str(newToken['_id'])
        AccessTokensDatabase.activeTokens.update_one(newToken, {"$set":{"code":code,"code_challenge":codeChallenge,"scope":scope}})
        return code
    #@staticmethod
    #def FindActiveToken(clientId, state, code,codeChallenge, scope):
    #    AccessTokensDatabase.activeTokens.find_one()
    


#AccessTokensDatabase.AddNewActiveToken("zxcvb","zxccc","azazazaz","lelelele")