from pydantic import BaseModel


class AudioMetaData(BaseModel):
    client_id: str
    sentence: str
    audio_file_name: str
    duration_ms: int
    surra_number: int
    aya_number: int


class AudioMetaDataIn(BaseModel):
    client_id: str
    sentence: str
    surra_number: int
    aya_number: int


class UploadOutSchema(BaseModel):
    file_name: str
