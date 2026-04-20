from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from skillrot_app.db.database import get_db
from skillrot_app.models.assessment import Assessment
from skillrot_app.models.subtopic import Subtopic
from skillrot_app.models.skill import Skill

from skillrot_app.services.file_parser_service import extract_text_from_file
from skillrot_app.services.assessment_analyzer_service import analyze_assessment_text
from skillrot_app.api.recommendations import clear_recommendation_cache

import json

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/{skill_id}")
async def upload_assessment(
    skill_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # --------------------------------------------------
    # 1️⃣ Extract Text (OCR / PDF / DOCX / CSV etc.)
    # --------------------------------------------------
    text = extract_text_from_file(file_bytes, file.filename)

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text")

    print("========== OCR EXTRACTED TEXT ==========")
    print(text)
    print("========================================")

    # --------------------------------------------------
    # 2️⃣ MASTER ANALYSIS (Generalized & Context-Aware)
    # --------------------------------------------------
    weak_topics = analyze_assessment_text(text, skill.name)

    # If nothing weak → raise an error for invalid file
    if not weak_topics:
        raise HTTPException(status_code=400, detail=f"Could not detect any relevant academic topics for the skill '{skill.name}'. Please upload an appropriate assessment containing missed questions for this specific skill.")

    # --------------------------------------------------
    # 3️⃣ SAFE SUBTOPIC UPDATE
    # --------------------------------------------------
    weak_subtopics_to_return = []
    
    for topic, severity in weak_topics.items():

        # Safety check (prevent dict crash)
        if not isinstance(severity, (int, float)):
            continue

        existing = (
            db.query(Subtopic)
            .filter(
                Subtopic.skill_id == skill_id,
                Subtopic.name.ilike(topic)
            )
            .first()
        )

        health_value = round((1 - severity) * 100, 2)
        weakness_percentage = round(severity * 100, 2)

        if existing:
            existing.health_score = health_value
        else:
            db.add(Subtopic(
                skill_id=skill_id,
                name=topic,
                health_score=health_value
            ))
            
        weak_subtopics_to_return.append({"topic": topic, "score": weakness_percentage})

    if weak_subtopics_to_return:
        clear_recommendation_cache(skill_id)

    # Store raw analysis result
    db.add(Assessment(
        skill_id=skill_id,
        parsed_result=json.dumps(weak_topics)
    ))

    db.commit()

    return {
        "skill_id": skill_id,
        "weak_topics": weak_subtopics_to_return,
        "stored": True
    }