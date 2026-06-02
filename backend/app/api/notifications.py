from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.database import get_db
from app.models import Notification
from app.schemas import NotificationRead

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    q = select(Notification).order_by(Notification.created_at.desc()).limit(limit)
    if unread_only:
        q = q.where(Notification.is_read == False)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/unread-count")
async def unread_count(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import func
    result = await db.execute(
        select(func.count(Notification.id)).where(Notification.is_read == False)
    )
    return {"count": result.scalar_one()}


@router.post("/{notification_id}/read", response_model=NotificationRead)
async def mark_read(notification_id: str, db: AsyncSession = Depends(get_db)):
    notif = await db.get(Notification, notification_id)
    if notif and not notif.is_read:
        notif.is_read = True
        notif.read_at = datetime.utcnow()
        await db.commit()
        await db.refresh(notif)
    return notif


@router.post("/read-all", status_code=204)
async def mark_all_read(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Notification).where(Notification.is_read == False))
    for notif in result.scalars().all():
        notif.is_read = True
        notif.read_at = datetime.utcnow()
    await db.commit()
