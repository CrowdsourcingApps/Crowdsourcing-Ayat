from pydantic import BaseModel


class AudioMetaData(BaseModel):
    client_id: str
    sentence: str
    audio_file_name: str
    duration_ms: int


class AudioMetaDataIn(BaseModel):
    client_id: str
    sentence: str


class UploadOutSchema(BaseModel):
    file_name: str
