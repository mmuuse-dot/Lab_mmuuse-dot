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
                # Ensure proper conversion and handle missing fields
                try:
                    assignments.append({
                        'assignment': row['assignment'],
                        'group': row['group'],
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except ValueError:
                    print(f"Invalid numeric value in row: {row}")
                    sys.exit(1)
                except KeyError:
                    print(f"Missing required column in CSV: {row}")
                    sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    print("\n--- Processing Grades ---")

    # A: Validate scores
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Invalid score in {item['assignment']}")
            return

    # B: Validate weights
    total_weight = sum(item['weight'] for item in data)
    formative_weight = sum(item['weight'] for item in data if item['group'] == "Formative")
    summative_weight = sum(item['weight'] for item in data if item['group'] == "Summative")

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
    final_grade = sum((item['score'] * item['weight']) / 100 for item in data)
    gpa = (final_grade / 100) * 5

    print(f"Final Grade: {final_grade:.2f}")
    print(f"GPA: {gpa:.2f}")

    # D: Pass/Fail
    formative_score = sum((item['score'] * item['weight']) / 100 for item in data if item['group'] == "Formative")
    summative_score = sum((item['score'] * item['weight']) / 100 for item in data if item['group'] == "Summative")

    formative_percent = (formative_score / 60) * 100
    summative_percent = (summative_score / 40) * 100

    status = "PASSED" if formative_percent >= 50 and summative_percent >= 50 else "FAILED"

    # E: Resubmission
    failed_formatives = [item for item in data if item['group'] == "Formative" and item['score'] < 50]

    resubmissions = []
    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        resubmissions = [item for item in failed_formatives if item['weight'] == max_weight]

    # F: Output
    print(f"\nFinal Status: {status}")

    if status == "FAILED" and resubmissions:
        print("\nResubmit the following assignment(s):")
        for item in resubmissions:
            print("-", item['assignment'])


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
