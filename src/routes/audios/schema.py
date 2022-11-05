from datetime import datetime

from pydantic import BaseModel


class AudioMetaDataIn(BaseModel):
    client_id: str
    sentence: str = None
    surra_number: int
    aya_number: int


class AudioMetaData(AudioMetaDataIn):
    audio_file_name: str
    duration_ms: int
    create_date: datetime = datetime.now()


class UploadOutSchema(BaseModel):
    file_name: str
