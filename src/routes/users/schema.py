from enum import Enum

from pydantic import BaseModel, validator

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
    country: CountryEnum = None
    qiraah: QiraahEnum = None
    platform: PlatformEnum

    @validator('age')
    def age_greater_than_six(cls, v):
        if v <= 6:
            raise ValueError('age must be greater than six')
        return v
