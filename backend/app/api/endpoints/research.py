"""
Research Notes API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import ResearchNote, User
from app.schemas.research import ResearchNoteCreate, ResearchNoteResponse
from app.api.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ResearchNoteResponse)
def create_research_note(
    note: ResearchNoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a research note"""
    new_note = ResearchNote(
        user_id=current_user.id,
        **note.dict()
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.get("/", response_model=List[ResearchNoteResponse])
def list_research_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all research notes for current user"""
    notes = db.query(ResearchNote).filter(
        ResearchNote.user_id == current_user.id
    ).order_by(ResearchNote.updated_at.desc()).all()

    return notes


@router.get("/{note_id}", response_model=ResearchNoteResponse)
def get_research_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific research note"""
    note = db.query(ResearchNote).filter(
        ResearchNote.id == note_id,
        ResearchNote.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Research note not found")

    return note
