import json
from src.ucr.ac.cr.models.recycling_record import RecyclingRecord

class RecyclingRecordRepository:

    def __init__(self, file_path="data/records.json"):
        self.file_path = file_path

    def get_all(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [RecyclingRecord.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_by_id(self, record_id: str):
        for record in self.get_all():
            if record.record_id == record_id:
                return record
        return None

    def add(self, record: RecyclingRecord):
        records = self.get_all()
        records.append(record)
        self.save_all(records)

    def save_all(self, records):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [record.to_dict() for record in records],
                file,
                indent=4,
                ensure_ascii=False
            )