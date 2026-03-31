import csv
import sys
import os

def load_csv_data():
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

        return assignments

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def evaluate_grades(data):
    print("\n--- Processing Grades ---")

    # A: Validate scores
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Invalid score in {item['assignment']}")
            return

    # B: Validate weights
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    for item in data:
        total_weight += item['weight']
        if item['group'] == "Formative":
            formative_weight += item['weight']
        else:
            summative_weight += item['weight']

    if total_weight != 100:
        print("Error: Total weight must be 100")
        return

    if formative_weight != 60:
        print("Error: Formative must be 60")
        return

    if summative_weight != 40:
        print("Error: Summative must be 40")
        return

    # C: Final grade & GPA
    final_grade = 0
    for item in data:
        final_grade += (item['score'] * item['weight']) / 100

    gpa = (final_grade / 100) * 5

    print(f"Final Grade: {final_grade:.2f}")
    print(f"GPA: {gpa:.2f}")

    # D: Pass/Fail

formative_total = 0
summative_total = 0

for item in data:
    if item['group'] == "Formative":
        formative_total += item['score'] * item['weight']
    else:
        summative_total += item['score'] * item['weight']

# Normalize properly
formative_percent = formative_total / 60
summative_percent = summative_total / 40

print(f"Formative %: {formative_percent:.2f}")
print(f"Summative %: {summative_percent:.2f}")

if formative_percent >= 50 and summative_percent >= 50:
    status = "PASSED"
else:
    status = "FAILED"
