import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.routes.audios.handler import add_audio
from src.routes.audios.helpers import upload_file, valid_file_size
from src.routes.audios.schema import (AudioMetaData, AudioMetaDataIn,
                                      UploadOutSchema)
from src.routes.users.handler import get_user
from src.routes.users.schema import PlatformEnum

router = APIRouter()


@router.post('',
             response_model=UploadOutSchema,
             status_code=200,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'},
                        404: {'description': 'NOT FOUND'}})
async def Add_new_audio(audio_meta_data: AudioMetaDataIn = Depends(),
                        audio_file: UploadFile = File(...)):
    audio_part = audio_file.filename.split('.')
    if len(audio_part) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="audio file name shoudn't contains dots",
        )

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
    # TODO depend on the platform check the extension of the audio file
    audio_extension = audio_part[1]
    if user.platform == PlatformEnum.IOS:
        if audio_extension != 'aac':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='only acc format is supported for IOS',
            )

    # TODO: limit file size and throw exception if it's too big
    max_upload_size = 2 * 1024 * 1024       # 2MB
    valid = valid_file_size(audio_file.file, max_upload_size)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The audio file shouldn't exced 2MB",
        )
    # TODO verified the content of the audio file using PyDub
    # upload the file to s3
    file_id = uuid.uuid4()
    new_file_name = str(file_id)+'.'+audio_extension
    # check that the file is uploaded successfully
    if upload_file(new_file_name, audio_file.file.fileno()):
        # calculate file size in ms. maybe we can do that in the begaining
        duration_ms = 10
        # send Meta data to firbase
        audio_meta_data = AudioMetaData(client_id=audio_meta_data.client_id,
                                        sentence=audio_meta_data.sentence,
                                        audio_file_name=new_file_name,
                                        duration_ms=duration_ms)
        if add_audio(file_id, dict(audio_meta_data)):
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
