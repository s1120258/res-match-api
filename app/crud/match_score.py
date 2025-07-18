# app/crud/match_score.py

from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
import logging
from app.models.match_score import MatchScore

logger = logging.getLogger(__name__)


def get_match_score(db: Session, job_id: UUID) -> Optional[MatchScore]:
    """Get match score for a specific job."""
    return db.query(MatchScore).filter(MatchScore.job_id == job_id).first()


def create_or_update_match_score(
    db: Session, job_id: UUID, resume_id: UUID, similarity_score: float
) -> MatchScore:
    """Create or update match score for a job."""
    existing_match = get_match_score(db, job_id)

    if existing_match:
        # Update existing record
        existing_match.similarity_score = similarity_score
        existing_match.resume_id = resume_id
        db.commit()
        db.refresh(existing_match)
        return existing_match
    else:
        # Create new record
        match_score = MatchScore(
            job_id=job_id,
            resume_id=resume_id,
            similarity_score=similarity_score,
        )
        db.add(match_score)
        db.commit()
        db.refresh(match_score)
        return match_score
