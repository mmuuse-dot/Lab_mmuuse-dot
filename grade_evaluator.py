import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
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
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Evaluates student grades by validating scores and weights,
    calculating GPA, determining pass/fail status,
    and identifying assignments eligible for resubmission.
    """
    print("\n--- Processing Grades ---")

    # Check if all scores are between 0 and 100
    for assignment in data:
        if assignment['score'] < 0 or assignment['score'] > 100:
            print(f"Error: '{assignment['assignment']}' has an invalid score of {assignment['score']}. Must be between 0 and 100.")
            sys.exit(1)
    print("All scores are valid.")

    #  Validate that all weights add up correctly
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    for assignment in data:
        total_weight += assignment['weight']
        if assignment['group'] == 'Formative':
            formative_weight += assignment['weight']
        elif assignment['group'] == 'Summative':
            summative_weight += assignment['weight']

    if total_weight != 100:
        print(f"Error: Total weights add up to {total_weight}, but must equal 100.")
        sys.exit(1)
    if formative_weight != 60:
        print(f"Error: Formative weights add up to {formative_weight}, but must equal 60.")
        sys.exit(1)
    if summative_weight != 40:
        print(f"Error: Summative weights add up to {summative_weight}, but must equal 40.")
        sys.exit(1)
    print("All weights are valid.")

    #  Calculate the final grade and GPA
    final_grade = 0
    formative_total = 0
    formative_weight_total = 0
    summative_total = 0
    summative_weight_total = 0

    for assignment in data:
        weighted_score = (assignment['score'] / 100) * assignment['weight']
        final_grade += weighted_score

        if assignment['group'] == 'Formative':
            formative_total += weighted_score
            formative_weight_total += assignment['weight']
        elif assignment['group'] == 'Summative':
            summative_total += weighted_score
            summative_weight_total += assignment['weight']

    gpa = (final_grade / 100) * 5.0
    formative_average = (formative_total / formative_weight_total) * 100
    summative_average = (summative_total / summative_weight_total) * 100

    #  Determine Pass/Fail status
    if formative_average >= 50 and summative_average >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    #  Find failed formative assignments eligible for resubmission
    failed_formative = []

    for assignment in data:
        if assignment['group'] == 'Formative' and assignment['score'] < 50:
            failed_formative.append(assignment)

    if failed_formative:
        highest_weight = 0
        for assignment in failed_formative:
            if assignment['weight'] > highest_weight:
                highest_weight = assignment['weight']

        resubmit = []
        for assignment in failed_formative:
            if assignment['weight'] == highest_weight:
                resubmit.append(assignment)
    else:
        resubmit = []

    # f) Print the final decision and resubmission options
    print("\n--- Final Decision ---")
    print(f"Final Grade: {final_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")
    print(f"Formative Average: {formative_average:.2f}%")
    print(f"Summative Average: {summative_average:.2f}%")
    print(f"Status: {status}")

    if resubmit:
        print("\nAssignment(s) eligible for resubmission:")
        for assignment in resubmit:
            print(f"  - {assignment['assignment']} (Score: {assignment['score']}, Weight: {assignment['weight']})")
    else:
        print("\nNo assignments eligible for resubmission.")

if __name__ == "__main__":
    #  Load the data
    course_data = load_csv_data()

    #  Process the features
    evaluate_grades(course_data)
