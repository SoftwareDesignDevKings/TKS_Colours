from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Application, Notification
from app.models.application import ApplicationStatus
from app.models.notification import NotificationType
from app.schemas import (
    ApplicationCreate, ApplicationRead, ApplicationUpdate, ApplicationDetail,
)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("", response_model=list[ApplicationDetail])
async def list_applications(
    status: Optional[str] = Query(None),
    club_id: Optional[str] = Query(None),
    student_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = (
        select(Application)
        .options(
            selectinload(Application.student),
            selectinload(Application.club),
        )
        .order_by(Application.applied_at.desc())
    )
    if status:
        q = q.where(Application.status == status)
    if club_id:
        q = q.where(Application.club_id == club_id)
    if student_id:
        q = q.where(Application.student_id == student_id)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=ApplicationRead, status_code=201)
async def create_application(payload: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    application = Application(
        student_id=payload.student_id,
        club_id=payload.club_id,
        notes=payload.notes,
        auto_triggered=payload.auto_triggered,
        status=ApplicationStatus.PENDING,
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


@router.get("/{app_id}", response_model=ApplicationDetail)
async def get_application(app_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Application)
        .where(Application.id == app_id)
        .options(
            selectinload(Application.student),
            selectinload(Application.club),
            selectinload(Application.reminders),
        )
    )
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")
    return app


@router.patch("/{app_id}", response_model=ApplicationRead)
async def update_application(
    app_id: str, payload: ApplicationUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Application).where(Application.id == app_id))
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    old_status = app.status
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(app, field, value)

    # Record decision timestamp when status changes to approved/rejected
    new_status = payload.status
    if new_status and new_status != old_status:
        if new_status in (ApplicationStatus.APPROVED, ApplicationStatus.REJECTED):
            if not payload.decided_by_id:
                raise HTTPException(
                    status_code=400, 
                    detail="A deciding staff member must be specified to decide this application."
                )
            from app.models.staff import Staff
            staff_result = await db.execute(select(Staff).where(Staff.id == payload.decided_by_id))
            staff = staff_result.scalars().first()
            if not staff:
                raise HTTPException(status_code=404, detail="Staff member not found.")
            if staff.role != "admin":
                raise HTTPException(
                    status_code=403, 
                    detail="Only the Head of Department (admin staff) can approve or reject applications."
                )
            app.decided_at = datetime.utcnow()
            # Create a notification for the decision
            notif_type = (
                NotificationType.APPLICATION_APPROVED
                if new_status == ApplicationStatus.APPROVED
                else NotificationType.APPLICATION_REJECTED
            )
            notification = Notification(
                type=notif_type,
                title=f"Application {new_status}",
                body=f"An application has been {new_status}.",
                student_id=app.student_id,
                application_id=app.id,
                club_id=app.club_id,
            )
            db.add(notification)

    await db.commit()
    await db.refresh(app)
    return app
