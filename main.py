import json
import os
from datetime import datetime

templates_file = 'templates.json'
workouts_file = 'workouts.json'

def load_templates():
    if os.path.exists(templates_file):
        with open(templates_file, 'r') as f:
            return json.load(f)
    return []

def load_workouts():
    if os.path.exists(workouts_file):
        with open(workouts_file, 'r') as f:
            return json.load(f)
    return []

def save_templates(templates):
    with open(templates_file, 'w') as f:
        json.dump(templates, f, indent=4)

def save_workouts(workouts):
    with open(workouts_file, 'w') as f:
        json.dump(workouts, f, indent=4)

def sort(workouts):
    workouts_sorted = workouts[:]
    for i in range(len(workouts_sorted)):
        for j in range(i + 1, len(workouts_sorted)):
            date_i = datetime.strptime(workouts_sorted[i]['date'], '%m/%d/%Y')
            date_j = datetime.strptime(workouts_sorted[j]['date'], '%m/%d/%Y')
            if date_i < date_j:
                workouts_sorted[i], workouts_sorted[j] = workouts_sorted[j], workouts_sorted[i]
    return workouts_sorted

def main():
    templates = load_templates()
    workouts = load_workouts()
    while True:
        print("\nWorkout Tracker\n")
        print("1. Create a Workout")
        print("2. View Workouts")
        print("3. Create a Workout Template\n")
        print("Keep track of your workouts so you can monitor your progress!\n")
        print("Create custom workout templates to track any exercise routine\n")
        print("Enter 'menu' at any time to return to this screen.\n")
        choice = input("Enter Option Number: ").strip()
        if choice.lower() == 'menu':
            continue
        elif choice == '1':
            create_workout(templates, workouts)
        elif choice == '2':
            view_workouts(workouts)
        elif choice == '3':
            create_template(templates)
        else:
            print("Invalid option")

def create_workout(templates, workouts):
    if not templates:
        print("No templates available")
        return
    print("\nChoose a template for this workout\n")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['name']}")
    print("\n")
    while True:
        choice = input("Enter Option Number: ").strip()
        if choice.lower() == 'menu':
            return
        index = int(choice) - 1
        if 0 <= index < len(templates):
            selected_template = templates[index]
            break
        else:
            print("Invalid option")
    date = datetime.now().strftime('%m/%d/%Y')
    workout = {
        "date": date,
        "template_name": selected_template['name'],
        "exercises": []
    }
    for exercise in selected_template['exercises']:
        while True:
            print(f"\nExercise: {exercise['name']}\n")
            print("Note: Measurement input will not be rounded to maintain precision.")
            print("Entering large numbers may cause the program to use extra resources.\n")
            value = input(f"Enter ({exercise['measurement']}): ").strip()
            if value.lower() == 'menu':
                return
            workout['exercises'].append({"name": exercise['name'], "value": value, "measurement": exercise['measurement']})
            break
    workouts.append(workout)
    save_workouts(workouts)
    print("Workout added")

def view_workouts(workouts):
    if not workouts:
        print("No workouts available")
        return
    workouts_sorted = sort(workouts)
    while True:
        print("\nWhich workout would you like to view?\n")
        for i, workout in enumerate(workouts_sorted, 1):
            print(f"{i}. {workout['template_name']}: {workout['date']}")
        print("\nEnter 'Remove: [Option Number]' to delete a workout\n")
        print("Removed workouts will not be retrievable\n")
        choice = input("Enter Option Number: ").strip()
        if choice.lower() == 'menu':
            return
        if 'remove:' in choice.lower():
            try:
                remove_index = int(choice.split(':')[1].strip()) - 1
                if 0 <= remove_index < len(workouts_sorted):
                    actual_index = workouts.index(workouts_sorted[remove_index])
                    del workouts[actual_index]
                    save_workouts(workouts)
                    print("Workout removed")
                    workouts_sorted = sort(workouts)
                else:
                    print("Invalid option")
            except (IndexError, ValueError):
                print("Invalid option")
            continue
        index = int(choice) - 1
        if 0 <= index < len(workouts_sorted):
            selected_workout = workouts_sorted[index]
            print("\nDate:", selected_workout['date'])
            print("Template:", selected_workout['template_name'])
            print("\n")
            for i, exercise in enumerate(selected_workout['exercises'], 1):
                print(f"Exercise {i}: {exercise['name']}")
                print(f"{exercise['measurement']}: {exercise['value']}\n")
            print("Enter 'Remove' to delete this workout\n")
            remove_choice = input("Enter 'menu' for main menu: ").strip().lower()
            if remove_choice == 'remove':
                actual_index = workouts.index(selected_workout)
                del workouts[actual_index]
                save_workouts(workouts)
                print("Workout removed.")
                return
            elif remove_choice == 'menu':
                return
            else:
                print("Invalid option")
        else:
            print("Invalid option")

def create_template(templates):
    print("\nCreate a new workout template\n")
    template_name = input("Enter Template Name: ").strip()
    if template_name.lower() == 'menu':
        return
    template = {
        "name": template_name,
        "exercises": []
    }
    print("\nCreate a new workout template\n")
    print(f"Template Name: {template_name}\n")
    print("Enter '[Exercise Name]:[Measurement]' to add an exercise\n")
    print("Enter 'done' to complete the template\n")
    print("Enter 'undo' if you no longer wish to create a template\n")
    while True:
        input_str = input("Input: ").strip()
        if input_str.lower() == 'menu':
            return
        elif input_str.lower() == 'done':
            if template['exercises']:
                templates.append(template)
                save_templates(templates)
                print("Template created")
                return
            else:
                print("Add at least one exercise")
        elif input_str.lower() == 'undo':
            print("Template creation cancelled")
            return
        else:
            exercise_name, measurement = input_str.split(':')
            exercise_name = exercise_name.strip()
            measurement = measurement.strip()
            if exercise_name and measurement:
                template['exercises'].append({"name": exercise_name, "measurement": measurement})
                print(f"Added exercise: {exercise_name} ({measurement})\n")
            else:
                print("Invalid input")

if __name__ == "__main__":
    main()