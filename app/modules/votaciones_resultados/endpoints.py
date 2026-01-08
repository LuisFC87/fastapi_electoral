from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, BackgroundTasks
from app.shared.dependencies import get_db
from app.modules.votaciones_resultados.repository import VotacionesRepository
from app.modules.votaciones_resultados.services import VotacionesService
from app.modules.votaciones_resultados import schemas
from app.modules.seguridad.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

router = APIRouter()

async def get_repo(db: AsyncSession = Depends(get_db)):
    return VotacionesRepository(db)

async def get_service(repo: VotacionesRepository = Depends(get_repo), db: AsyncSession = Depends(get_db)):
    return VotacionesService(repo, db)

@router.post('/actas', response_model=schemas.ActaUploadResponse)
async def upload_acta(background_tasks: BackgroundTasks, file: UploadFile = File(...), proceso_id: int = Form(...), mesa_id: int = Form(...), idempotency_key: Optional[str] = Form(None), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    content = await file.read()
    imagen_url = f"/storage/{file.filename}"
    repo = VotacionesRepository(db)
    svc = VotacionesService(repo, db)
    acta = await svc.upload_acta(content, imagen_url, mesa_id, proceso_id, idempotency_key, uploaded_by=current_user.id)
    return {
        'id': acta.id,
        'status': acta.status,
        'idempotency_key': acta.idempotency_key,
        'checksum': acta.checksum,
        'imagen_url': acta.imagen_url,
        'created_at': acta.created_at
    }

@router.get('/actas/{acta_id}', response_model=schemas.ActaRawRead)
async def get_acta(acta_id: int, repo: VotacionesRepository = Depends(get_repo)):
    acta = await repo.get_acta_raw(acta_id)
    if not acta:
        raise HTTPException(status_code=404, detail='Acta no encontrada')
    return acta

@router.post('/actas/{processed_id}/validate')
async def validate_acta(processed_id: int, payload: schemas.ValidatePayload, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    repo = VotacionesRepository(db)
    svc = VotacionesService(repo, db)
    processed = await svc.validate_acta(processed_id, payload, usuario_id=current_user.id)
    return {'ok': True, 'processed_id': processed.id, 'validated': processed.validated}

@router.get('/resultados/mesa/{mesa_id}')
async def resultados_mesa(mesa_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, func
    from app.modules.votaciones_resultados import models
    q = select(models.Resultado.partido_id, func.sum(models.Resultado.votos)).join(models.ActaProcessed).join(models.ActaRaw).where(models.ActaRaw.mesa_id==mesa_id, models.ActaProcessed.validated==True).group_by(models.Resultado.partido_id)
    r = await db.execute(q)
    rows = r.all()
    return {'mesa_id': mesa_id, 'by_party': [{'partido_id': row[0], 'votos': int(row[1])} for row in rows]}

@router.get('/resultados/aggregate')
async def resultados_aggregate(proceso_id: Optional[int]=None, cargo_id: Optional[int]=None, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, func
    from app.modules.votaciones_resultados import models
    q = select(models.Resultado.partido_id, func.sum(models.Resultado.votos)).join(models.ActaProcessed).join(models.ActaRaw).where(models.ActaProcessed.validated==True)
    if proceso_id:
        q = q.where(models.ActaRaw.proceso_id==proceso_id)
    q = q.group_by(models.Resultado.partido_id)
    r = await db.execute(q)
    rows = r.all()
    totals = {'votos_validos': sum([int(row[1]) for row in rows])}
    by_party = [{'partido_id': row[0], 'votos': int(row[1])} for row in rows]
    return {'totals': totals, 'by_party': by_party}
