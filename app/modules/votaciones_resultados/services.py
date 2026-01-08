from app.modules.votaciones_resultados.repository import VotacionesRepository
from app.core.errors import BusinessException
from app.modules.votaciones_resultados import schemas
from typing import Optional, List
import hashlib

class VotacionesService:
    def __init__(self, repo: VotacionesRepository, db):
        self.repo = repo
        self.db = db

    async def upload_acta(self, file_bytes: bytes, imagen_url: str, mesa_id: int, proceso_id: int, idempotency_key: Optional[str], uploaded_by: Optional[int]=None):
        checksum = hashlib.sha256(file_bytes).hexdigest()
        if idempotency_key:
            existing = await self.repo.find_by_idempotency(proceso_id, mesa_id, idempotency_key)
            if existing:
                return existing
        acta = await self.repo.create_acta_raw(imagen_url=imagen_url, checksum=checksum, mesa_id=mesa_id, proceso_id=proceso_id, idempotency_key=idempotency_key, uploaded_by=uploaded_by)
        return acta

    async def process_acta(self, acta_id: int, processor: str, ocr_json: dict, resultados: List[schemas.ResultadoItem]):
        acta = await self.repo.get_acta_raw(acta_id)
        if not acta:
            raise BusinessException('Acta no encontrada', code=404)
        await self.repo.mark_processing(acta)
        for r in resultados:
            if r.votos < 0:
                await self.repo.add_validacion(acta.id, 'votos_no_negativos', False, f'Votos negativos para candidato/partido', 'ERROR')
                raise BusinessException('Votos negativos detectados', code=400)
        processed = await self.repo.create_processed(acta, processor, ocr_json, resultados)
        return processed

    async def validate_acta(self, processed_id: int, payload: schemas.ValidatePayload, usuario_id: Optional[int]=None):
        from sqlalchemy import select
        from app.modules.votaciones_resultados import models
        q = select(models.ActaProcessed).where(models.ActaProcessed.id==processed_id)
        r = await self.db.execute(q)
        processed = r.scalar_one_or_none()
        if not processed:
            raise BusinessException('Acta procesada no encontrada', code=404)
        processed.validated = payload.validated
        await self.db.flush()
        await self.db.commit()
        return processed
