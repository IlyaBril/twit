from fastapi import APIRouter, HTTPException, Response, UploadFile
from sqlmodel import delete, select

from app.models.models import Media, SessionDep

app_medias = APIRouter()


@app_medias.get(
    "/{media_id}",
)
async def media_receive(session: SessionDep, media_id):
    media = session.execute(select(Media.file_body).where(Media.id == media_id)).one()
    return Response(content=media.file_body, media_type="image/png")


@app_medias.post("/")
async def media_add(session: SessionDep, file: UploadFile) -> dict:

    file_name = file.filename
    file_body = await file.read()

    media_f = Media(file_name=file_name, file_body=file_body)
    session.add(media_f)
    session.commit()
    session.refresh(media_f)
    return {"result": True, "media_id": media_f.id}


@app_medias.delete(
    "/{media_id}",
)
async def media_delete(session: SessionDep, media_id):
    if media_id is None:
        raise HTTPException(status_code=404, detail="media_id absent")
    del_media = session.execute(select(Media, int(media_id))).one_or_none()
    if del_media:
        session.execute(delete(del_media))
        session.commit()
    return "", 202
