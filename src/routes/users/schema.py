from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from src.settings import countries


class CountryEnum(str, Enum):
    pass


CountryEnum = CountryEnum('CountryEnum', dict(countries))


class GenderEnum(str, Enum):
    Male = 'male'
    Female = 'female'


class QiraahEnum(str, Enum):
    Hafs = 'hafs'
    Warsh = 'warsh'
    Qaloon = 'qaloon'
    Other = 'other'
    DontKnow = 'dont_know'


class PlatformEnum(str, Enum):
    IOS = 'ios'
    Android = 'android'
    Web = 'web'


class AgeEnum(str, Enum):
    Under_14 = 'under_14'
    between_14_18 = '14-18'
    between_19_24 = '19-24'
    between_25_32 = '25-32'
    between_33_40 = '33-40'
    Above_40 = 'above_40'


class UserMetaDataCreate(BaseModel):
    age: AgeEnum = None
    gender: GenderEnum = None
    country: CountryEnum = None
    qiraah: QiraahEnum = None
    platform: PlatformEnum


class UserMetaData(UserMetaDataCreate):
    create_date: datetime = None
    client_id: str
    application_id: str = None
