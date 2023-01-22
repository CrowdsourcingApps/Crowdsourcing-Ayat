from datetime import datetime

from pydantic import BaseModel


class CommonControltask(BaseModel):
    recording_id: str
    surra_number: int
    aya_number: int
    audio_file_name: str
    duration_ms: int
    create_date: datetime = None
    surra_aya: str
    golden: bool  # is labeled by experts or labeled by crowd
