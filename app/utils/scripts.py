import csv
from datetime import datetime
from app.models.subjects import Subject

def load_subjects_from_csv():
    file_patch = 'preload/subjects.csv'
    with open(file_patch, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Crear un objeto Subject con los datos del CSV
            prerequisites = []
            prerequisite_codes = [code.strip() for code in row['prerequisites'].split(',')]

            if Subject.objects(code=row['code']).first():
                print(f"Materia ya éxiste {row['code']}")
                continue

            for code in prerequisite_codes:
                prerequisite = Subject.objects(code=code).first()
                if prerequisite:
                    prerequisites.append(prerequisite)
                else:
                    print(f"El requisito previo '{code}' para la materia '{row['code']}' no existe.")

            subject = Subject(
                code=row['code'],
                name=row['name'],
                semester=row['semester'],
                credits=int(row['credits']),
                prerequisites=prerequisites,
            )
            subject.save()
