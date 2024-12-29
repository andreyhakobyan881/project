from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import join, func
import uvicorn
from initdb import *
from datetime import datetime

app = FastAPI()
@app.post("/sport_types/")
def create_sport_type(sport_type: SportTypeModel):
    db = get_db()
    db.add(sport_type)
    db.commit()
    db.refresh(sport_type)

@app.get("/sport_types/")
def read_sport_types():
    return get_db().query(SportType).all()

@app.get("/sport_types/{sport_type_id}")
def read_sport_type(sport_type_id: int):
    db = get_db()
    sport_type = db.query(SportType).filter(SportType.id == sport_type_id).first()
    if not sport_type:
        raise HTTPException(status_code=404, detail="Sport Type not found")
    return sport_type

@app.delete("/sport_types/{sport_type_id}")
def delete_sport_type(sport_type_id: int):
    db = get_db()
    sport_type = db.query(SportType).filter(SportType.id == sport_type_id).first()
    if not sport_type:
        raise HTTPException(status_code=404, detail="Sport Type not found")
    db.delete(sport_type)
    db.commit()
    return {"detail": "Sport Type deleted"}

@app.post("/athletes_create/")
def create_athlete(athlete: AthleteModel):
    db = get_db()
    db.add(athlete)
    db.commit()
    db.refresh(athlete)

@app.get("/athletes_read/")
def read_athletes():
    db = get_db()
    return db.query(Athlete).all()

@app.get("/athletes/{athlete_id}")
def read_athlete(athlete_id: int):
    db = get_db()
    athlete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    return athlete

@app.delete("/delete_athletes/{athlete_id}")
def delete_athlete(athlete_id: int):
    db = get_db()
    athlete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    db.delete(athlete)
    db.commit()
    return {"detail": "Athlete deleted"}

@app.post("/results/")
def create_result(result: ResultModel):
    db = get_db()
    db.add(result)
    db.commit()
    db.refresh(result)

@app.get("/results/")
def read_results():
    db = get_db()
    return db.query(Result).all()

@app.get("/results/{result_id}")
def read_result(result_id: int):
    db = get_db()
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

@app.delete("/results/{result_id}")
def delete_result(result_id: int):
    db = get_db()
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(result)
    db.commit()
    return {"detail": "Result deleted"}

@app.get("/expired_records/")
def get_expired_records():
    db = get_db()
    today = datetime.now().date()
    expired_records = db.query(Result).filter(Result.competition_date < today).all()
    return expired_records

@app.get("/top_athletes/")
def get_top_athletes(min_victories: int):
    db = get_db()
    athletes = db.query(Athlete).filter(Athlete.victories >= min_victories).all()
    return athletes

@app.put("/update_record/")
def update_record(sport_name: str, athlete_name: str, percentage: float):
    db = get_db()
    joined = join(Result, Athlete, Result.athlete_id == Athlete.id).join(SportType, Result.sport_type_id == SportType.id)
    result = (
        db.query(Result)
        .select_from(joined)
        .filter(SportType.name == sport_name, Athlete.full_name == athlete_name)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Result with given sport and athlete not found")

    result.result_value -= result.result_value * (percentage / 100)
    db.commit()
    db.refresh(result)

    return {"message": "Record updated successfully", "new_value": result.result_value}


@app.get("/popular_sportsman/")
def get_popular_sportsman(min_victories: int):
    db = get_db()
    result = (
        db.query(Athlete, func.count(Result.id).label("victory_count"))
        .join(Result, Athlete.id == Result.athlete_id)
        .group_by(Athlete.id)
        .having(func.count(Result.id) >= min_victories)
        .all()
    )

    sportsmen = [{"athlete": athlete, "victory_count": victory_count} for athlete, victory_count in result]
    return sportsmen


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
