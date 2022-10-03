from enum import Enum

from pydantic import BaseModel


class GenderEnum(str, Enum):
    Male = 'male'
    Female = 'female'


class QiraahEnum(str, Enum):
    Hafs = 'hafs'
    Warsh = 'warsh'
    Kalon = 'kalon'
    Other = 'other'
    DontKnow = 'dont_know'


class PlatformEnum(str, Enum):
    IOS = 'ios'
    Android = 'android'
    Web = 'web'


class UserMetaData(BaseModel):
    client_id: str
    age: int = None
    gender: GenderEnum = None
    country: str = None
    qiraah: QiraahEnum = None
    platform: PlatformEnum
