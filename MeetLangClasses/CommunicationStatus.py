from enum import Enum

class StatusEnum(Enum):
    NonExistingUser = -4
    InactiveToken = -3
    UnregisteredClient = -2
    WrongPassword = -1
    UndefinedFail = 0
    Success = 1

class CommunicationStatus():
    @staticmethod
    def Success(additionalData):
        return {"status": StatusEnum.Success, **additionalData}
    @staticmethod
    def WrongPassword():
        return {"status": StatusEnum.WrongPassword}
    @staticmethod
    def UnregisteredClient():
        return {"status": StatusEnum.UnregisteredClient}
    @staticmethod
    def InactiveToken():
        return {"status": StatusEnum.InactiveToken}
    @staticmethod
    def NonExistingUser():
        return {"status": StatusEnum.NonExistingUser}
    @staticmethod
    def UndefinedFail():
        return {"status": StatusEnum.UndefinedFail}