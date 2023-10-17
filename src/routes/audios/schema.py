from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LabelEnum(str, Enum):
    Correct = 'correct'
    InCorrect = 'in_correct'
    NotRelatedToQuran = 'not_related_quran'
    NotMatchAya = 'not_match_aya'
    MultipleAya = 'multiple_aya'
    InComplete = 'in_complete'


class AudioMetaDataIn(BaseModel):
    client_id: str
    sentence: str = None
    surra_number: int
    aya_number: int


class AudioMetaData(AudioMetaDataIn):
    audio_file_name: str
    duration_ms: int
    create_date: datetime = None
    surra_aya: str = None
    transfared: bool = None
    label: LabelEnum = None


class UploadOutSchema(BaseModel):
    file_name: str


class AudioStateSchema(BaseModel):
    label: LabelEnum = None
