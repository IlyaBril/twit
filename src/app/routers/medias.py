from fastapi import (APIRouter,
                     UploadFile,
                     Response,
                     )

from app.models.models import (
                        Media,
                        SessionDep,
                        )

from sqlmodel import (select, delete)

app_medias = APIRouter()

@app_medias.get("/{media_id}",)
async def media_receive(session: SessionDep, media_id):
    media = session.execute(select(Media.file_body).where(Media.id==media_id)).one()
    return Response(content=media.file_body, media_type="image/png")


@app_medias.post("/")
async def media_add(session: SessionDep,
                    file: UploadFile | None = None) -> dict:

    file_name = file.filename
    file_body = await file.read()

    media_f = Media(file_name=file_name, file_body=file_body)
    session.add(media_f)
    session.commit()
    session.refresh(media_f)
    return {"result": True,
            "media_id": media_f.id}


@app_medias.delete("/{media_id}",)
async def media_receive(session: SessionDep, media_id):
    session.execute(delete(Media).where(Media.id==int(media_id)))
    session.commit()
    return '', 202
