from initdb import *
from datetime import datetime

def populate_database():
    db = get_db()

    
    sport_types = [
    SportType(name="100m Sprint", unit="seconds", world_record=9.58, olympic_record=9.63, searchable_data="{\"name\":\"Usain Bolt \", \"country\":\"Jamaica\"}"),
    SportType(name="Long Jump", unit="meters", world_record=8.95, olympic_record=8.90, searchable_data="{\"athlete\":\"Carl Lewis\", \"record\":8.91}"),
    SportType(name="High Jump", unit="meters", world_record=2.45, olympic_record=2.39, searchable_data="{\"athlete\":\"Javier Sotomayor\", \"record\":2.45}"),
    SportType(name="Marathon", unit="hours", world_record=2.01, olympic_record=2.06, searchable_data="{\"athlete\":\"Eliud Kipchoge\", \"record\":2.01}"),
    SportType(name="Shot Put", unit="meters", world_record=23.37, olympic_record=22.52, searchable_data="{\"athlete\":\"Ryan Crouser\", \"record\":23.30}")
]
    db.add_all(sport_types)
    db.commit()

    
    athletes = [
        Athlete(full_name="Usain Bolt", country="Jamaica", birth_year=1986, victories=8),
        Athlete(full_name="Carl Lewis", country="USA", birth_year=1961, victories=9),
        Athlete(full_name="Allyson Felix", country="USA", birth_year=1985, victories=11),
        Athlete(full_name="Eliud Kipchoge", country="Kenya", birth_year=1984, victories=5),
        Athlete(full_name="Ryan Crouser", country="USA", birth_year=1992, victories=15),
    ]
    db.add_all(athletes)
    db.commit()

   
    results = [
        Result(sport_type_id=1, athlete_id=1, competition_name="Olympics 2008", result_value=9.69, 
               competition_date=datetime(2008, 8, 16).date(), location="Beijing"),
        Result(sport_type_id=1, athlete_id=1, competition_name="Olympics 2012", result_value=9.63, 
               competition_date=datetime(2012, 8, 5).date(), location="London"),
        Result(sport_type_id=2, athlete_id=2, competition_name="World Championship 1991", result_value=8.91, 
               competition_date=datetime(1991, 8, 30).date(), location="Tokyo"),
        Result(sport_type_id=3, athlete_id=3, competition_name="Olympics 2004", result_value=2.35, 
               competition_date=datetime(2004, 8, 28).date(), location="Athens"),
        Result(sport_type_id=4, athlete_id=4, competition_name="Berlin Marathon 2018", result_value=2.01, 
               competition_date=datetime(2018, 9, 16).date(), location="Berlin"),
        Result(sport_type_id=5, athlete_id=5, competition_name="Olympics 2025", result_value=23.30, 
               competition_date=datetime(2025, 8, 5).date(), location="Tokyo"),
    ]
    db.add_all(results)
    db.commit()

if __name__ == "__main__":
    populate_database()
