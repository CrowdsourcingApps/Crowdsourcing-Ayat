from pydantic import BaseModel


class AudioMetaData(BaseModel):
    client_id: str
    sentence: str = None
    audio_file_name: str
    duration_ms: int
    surra_number: int
    aya_number: int


class AudioMetaDataIn(BaseModel):
    client_id: str
    sentence: str = None
    surra_number: int
    aya_number: int


class UploadOutSchema(BaseModel):
    file_name: str
