from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.votaciones_resultados import models, schemas

class VotacionesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_idempotency(self, proceso_id: int, mesa_id: int, idempotency_key: str) -> Optional[models.ActaRaw]:
        q = select(models.ActaRaw).where(models.ActaRaw.proceso_id==proceso_id, models.ActaRaw.mesa_id==mesa_id, models.ActaRaw.idempotency_key==idempotency_key)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def create_acta_raw(self, imagen_url: str, checksum: str, mesa_id: int, proceso_id: int, idempotency_key: Optional[str], uploaded_by: Optional[int]=None) -> models.ActaRaw:
        obj = models.ActaRaw(imagen_url=imagen_url, checksum=checksum, mesa_id=mesa_id, proceso_id=proceso_id, idempotency_key=idempotency_key, uploaded_by=uploaded_by, status='CARGADA')
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        await self.session.commit()
        return obj

    async def get_acta_raw(self, acta_id: int) -> Optional[models.ActaRaw]:
        q = select(models.ActaRaw).where(models.ActaRaw.id==acta_id)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def mark_processing(self, acta: models.ActaRaw):
        acta.status = 'PROCESSING'
        self.session.add(acta)
        await self.session.flush()
        await self.session.commit()
        return acta

    async def create_processed(self, acta_raw: models.ActaRaw, processor: str, ocr_json: dict, resultados: List[schemas.ResultadoItem]):
        processed = models.ActaProcessed(acta_raw_id=acta_raw.id, processor=processor, ocr_json=ocr_json)
        self.session.add(processed)
        await self.session.flush()
        for r in resultados:
            res = models.Resultado(acta_processed_id=processed.id, candidato_id=r.candidato_id, partido_id=r.partido_id, votos=r.votos)
            self.session.add(res)
        await self.session.flush()
        await self.session.refresh(processed)
        acta_raw.status = 'PROCESSED'
        self.session.add(acta_raw)
        await self.session.commit()
        return processed

    async def list_processed_for_acta(self, acta_raw_id: int):
        q = select(models.ActaProcessed).where(models.ActaProcessed.acta_raw_id==acta_raw_id).order_by(models.ActaProcessed.version.desc())
        r = await self.session.execute(q)
        return r.scalars().all()

    async def add_validacion(self, acta_id: int, regla: str, resultado: bool, mensaje: str, nivel: str='ERROR', usuario_id: Optional[int]=None):
        v = models.ValidacionActa(acta_id=acta_id, regla=regla, resultado=resultado, mensaje=mensaje, nivel=nivel, usuario_id=usuario_id)
        self.session.add(v)
        await self.session.flush()
        await self.session.commit()
        return v
