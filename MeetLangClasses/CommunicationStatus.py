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
        return {"status": StatusEnum.Success.value, **additionalData}
    @staticmethod
    def WrongPassword():
        return {"status": StatusEnum.WrongPassword.value}
    @staticmethod
    def UnregisteredClient():
        return {"status": StatusEnum.UnregisteredClient.value}
    @staticmethod
    def InactiveToken():
        return {"status": StatusEnum.InactiveToken.value}
    @staticmethod
    def NonExistingUser():
        return {"status": StatusEnum.NonExistingUser.value}
    @staticmethod
    def UndefinedFail():
        return {"status": StatusEnum.UndefinedFail.value}