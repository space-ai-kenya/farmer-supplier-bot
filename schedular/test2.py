from datetime import datetime, timedelta
from pydantic import BaseModel,Field,validator

from datetime import datetime, timedelta
from enum import Enum

class IntervalType(Enum):
    DAILY = 1
    WEEKLY = 2
    BI_WEEKLY = 3
    MONTHLY = 4

class Vaccination(BaseModel):
    vaccine_name: str
    vaccination_date: str
    dosage: float
    cow_id: str

class ScheduledVaccination:
    def __init__(self, vaccination, next_date, interval_type):
        self.vaccination = vaccination
        self.next_date = next_date
        self.interval_type = interval_type

class VaccinationScheduler:
    def __init__(self):
        self.scheduled_vaccinations = []

    def schedule_vaccination(self, vaccination, interval_type, interval_value):
        next_date = datetime.strptime(vaccination.vaccination_date, "%Y-%m-%d")
        if interval_type == IntervalType.DAILY:
            next_date += timedelta(days=interval_value)
        elif interval_type == IntervalType.WEEKLY:
            next_date += timedelta(weeks=interval_value)
        elif interval_type == IntervalType.BI_WEEKLY:
            next_date += timedelta(weeks=interval_value * 2)
        elif interval_type == IntervalType.MONTHLY:
            next_date += timedelta(days=interval_value * 30)

        scheduled_vaccination = ScheduledVaccination(vaccination, next_date, interval_type)
        self.scheduled_vaccinations.append(scheduled_vaccination)

    def send_alerts(self):
        today = datetime.now().date()
        for scheduled_vaccination in self.scheduled_vaccinations:
            if scheduled_vaccination.next_date.date() == today:
                interval_string = self.get_interval_string(scheduled_vaccination.interval_type)
                print(f"Alert: It's time to vaccinate cow {scheduled_vaccination.vaccination.cow_id} with {scheduled_vaccination.vaccination.vaccine_name} (Dosage: {scheduled_vaccination.vaccination.dosage}). Next vaccination in {interval_string}.")

    def get_interval_string(self, interval_type):
        if interval_type == IntervalType.DAILY:
            return "1 day"
        elif interval_type == IntervalType.WEEKLY:
            return "1 week"
        elif interval_type == IntervalType.BI_WEEKLY:
            return "2 weeks"
        elif interval_type == IntervalType.MONTHLY:
            return "1 month"

# Example usage
vaccination1 = Vaccination(
    vaccine_name="Bovine Viral Diarrhea Vaccine",
    vaccination_date="2023-03-28",
    dosage=2.5,
    cow_id="ABC123"
)

vaccination2 = Vaccination(
    vaccine_name="Foot and Mouth Disease Vaccine",
    vaccination_date="2023-03-28",
    dosage=3.0,
    cow_id="DEF456"
)

scheduler = VaccinationScheduler()
scheduler.schedule_vaccination(vaccination1, IntervalType.BI_WEEKLY, 2)  # Schedule next vaccination after 4 weeks
scheduler.schedule_vaccination(vaccination2, IntervalType.MONTHLY, 6)  # Schedule next vaccination after 6 months

# Send alerts for today's scheduled vaccinations
scheduler.send_alerts()