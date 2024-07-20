from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from minio import Minio, S3Error

from minio_microservice.files.dependencies import (
    get_minio_client,
)
from minio_microservice.micro_config import config

router = APIRouter(prefix='/minio', tags=['MinIO'])


@router.get('/download/{filename}')
async def download(
    filename: str,
    client: Minio = Depends(get_minio_client),
):
    response = client.get_object(config.bucket_name, filename)
    return StreamingResponse(response, media_type='application/octet-stream')


@router.post('/upload', status_code=status.HTTP_201_CREATED)
def upload(
    file: UploadFile,
    filename: str = Form(...),
    client: Minio = Depends(get_minio_client),
) -> dict:
    client.put_object(
        config.bucket_name,
        filename,
        data=file.file,
        length=file.size,
    )

    return {'details': f'Saved file: {filename}'}


@router.delete('/delete/{filename}')
def delete(filename: str, client: Minio = Depends(get_minio_client)):
    try:
        client.remove_object(config.bucket_name, filename)

        return {'details': f'Deleted file: {filename}'}
    except S3Error as exc:
        raise HTTPException(
            status_code=404, detail=f'File not found: {filename}'
        ) from exc
