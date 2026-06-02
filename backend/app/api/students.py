from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import csv
import io
from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentRead, StudentUpdate, StudentSummary

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentSummary])
async def list_students(
    year_group: Optional[int] = Query(None, ge=7, le=12),
    is_active: Optional[bool] = Query(True),
    search: Optional[str] = Query(None, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(Student)
    if year_group is not None:
        q = q.where(Student.year_group == year_group)
    if is_active is not None:
        q = q.where(Student.is_active == is_active)
    if search:
        q = q.where(
            Student.name.ilike(f"%{search}%") | Student.email.ilike(f"%{search}%")
        )
    q = q.order_by(Student.year_group, Student.name)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=StudentRead, status_code=201)
async def create_student(payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Student).where(Student.email == payload.email))
    if existing.scalars().first():
        raise HTTPException(status_code=409, detail="A student with this email already exists.")
    student = Student(**payload.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.post("/bulk-import", status_code=201)
async def bulk_import_students(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Must be a CSV file")
        
    contents = await file.read()
    try:
        text = contents.decode('utf-8-sig') # Handle optional BOM
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding")
        
    reader = csv.DictReader(io.StringIO(text))
    expected_fields = {"name", "email", "year_group", "cohort_year"}
    
    # Handle cases where DictReader fieldnames might be None or missing spaces
    actual_fields = {f.strip().lower() for f in (reader.fieldnames or [])}
    if not expected_fields.issubset(actual_fields):
        raise HTTPException(status_code=400, detail=f"CSV must contain headers: {', '.join(expected_fields)}")
        
    # Standardize headers in the dict
    reader.fieldnames = [f.strip().lower() for f in (reader.fieldnames or [])]
        
    created_count = 0
    errors = []
    
    for row_idx, row in enumerate(reader, start=2): # 1 is header
        try:
            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            if not name or not email:
                errors.append(f"Row {row_idx}: Name and email are required")
                continue
                
            year_group = int(row.get("year_group", "0").strip())
            cohort_year = int(row.get("cohort_year", "0").strip())
            
            if not (7 <= year_group <= 12):
                errors.append(f"Row {row_idx}: Year group must be between 7 and 12")
                continue
            
            # Check if email exists
            existing = await db.execute(select(Student).where(Student.email == email))
            if existing.scalars().first():
                errors.append(f"Row {row_idx}: Email {email} already exists")
                continue
                
            student = Student(name=name, email=email, year_group=year_group, cohort_year=cohort_year)
            db.add(student)
            created_count += 1
            
        except ValueError:
            errors.append(f"Row {row_idx}: Invalid number format for year_group or cohort_year")
        except Exception as e:
            errors.append(f"Row {row_idx}: {str(e)}")
            
    await db.commit()
    return {"message": f"Successfully imported {created_count} students", "errors": errors}



@router.get("/{student_id}", response_model=StudentRead)
async def get_student(student_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@router.patch("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: str, payload: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    # Soft delete
    student.is_active = False
    await db.commit()
