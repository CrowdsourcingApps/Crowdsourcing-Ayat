import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.routes.audios.handler import add_audio
from src.routes.audios.helpers import process_audio, upload_file
from src.routes.audios.schema import (AudioMetaData, AudioMetaDataIn,
                                      UploadOutSchema)
from src.routes.users.handler import get_user
from src.settings.logging import logger

router = APIRouter()


@router.post('',
             response_model=UploadOutSchema,
             status_code=200,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'},
                        404: {'description': 'NOT FOUND'}})
async def Add_new_audio(audio_meta_data: AudioMetaDataIn = Depends(),
                        audio_file: UploadFile = File(...)):
    if not audio_file.content_type.startswith('audio'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='audio only is allowed',
        )
    # make sure that client id info is existed in users node
    user = get_user(audio_meta_data.client_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no client with id {audio_meta_data.client_id}',
        )

    # limit audio file length and throw exception if it's too long
    # Standarize audio file: wav, 16000Hz, one channel
    max_audio_length = 30000       # 30 sec
    min_audio_length = 500         # 0.5 sec
    try:
        audio_length_ms, wav_file = process_audio(audio_file.file)
    except Exception as ex:
        logger.exception(f'[Pydub] - Unable to process audio file: {ex}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unable to process the audio file {audio_file.filename}',
        )
    if audio_length_ms > max_audio_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The audio file shouldn't exced 30 Sec",
        )
    if audio_length_ms < min_audio_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The audio file shouldn't be less than 0.5 Sec",
        )
    file_id = uuid.uuid4()
    new_file_name = str(file_id)+'.wav'

    # upload the file to s3 and check that the file is uploaded successfully
    if upload_file(new_file_name, wav_file):
        # send Meta data to firbase
        surra_number = audio_meta_data.surra_number
        aya_number = audio_meta_data.aya_number
        surra_aya = str(surra_number)+'-'+str(aya_number)
        audio_meta_data = AudioMetaData(client_id=audio_meta_data.client_id,
                                        sentence=audio_meta_data.sentence,
                                        audio_file_name=new_file_name,
                                        duration_ms=audio_length_ms,
                                        surra_number=surra_number,
                                        aya_number=aya_number,
                                        create_date=datetime.now(),
                                        surra_aya=surra_aya,
                                        transfared=False)
        audio_dict = dict(audio_meta_data)
        audio_dict['create_date'] = str(audio_dict['create_date'])
        if add_audio(file_id, audio_dict):
            return {'file_name': new_file_name}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='audio meta data was not saved successfully',
            )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='audio file was not uploaded successfully',
    )
