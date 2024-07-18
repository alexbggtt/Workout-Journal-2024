from CrudOperations import Operations
import pandas as pd

exercise_matrix = {
    1: 'Shoulder Press',
    2: 'Shoulder Press Unilateral Left',
    3: 'Shoulder Press Unilateral Right',
    4: 'Lateral Raise',
    5: 'Lateral Raise Unilateral Left',
    6: 'Lateral Raise Unilateral Right',
    7: 'Front Raise',
    8: 'Rear Deltoid Fly',
    9: 'Lat Pull-down',
    10: 'Lat Pull-down Inward-Grip',
    11: 'Lat Pull-down Reverse Grip',
    12: 'Lat Pull-down Unilateral Left',
    13: 'Lat Pull-down Unilateral Right',
    14: 'Lat Push-Down',
    15: 'Row',
    16: 'Row Unilateral Left',
    17: 'Row Unilateral Right',
    18: 'Pull-up',
    19: 'Bench Press',
    20: 'Push-up',
    21: 'Dip',
    22: 'Incline Press',
    23: 'Decline Press',
    24: 'Dumbbell Press',
    25: 'Dumbbell Press Unilateral Left',
    26: 'Dumbbell Press Unilateral Right',
    27: 'Pec Fly',
    28: 'Dumbbell Fly',
    29: 'Dumbbell Pec Circle',
    30: 'Bicep Curl',
    31: 'Bicep Curl Unilateral Left',
    32: 'Bicep Curl Unilateral Right',
    33: 'Tricep Extension',
    34: 'Tricep Extension Unilateral Left',
    35: 'Tricep Extension Unilateral Right',
    36: 'Hammer Curl',
    37: 'Squat',
    38: 'Bulgarian Squat',
    39: 'Lunge',
    40: 'Walking Lunge',
    41: 'Leg Press',
    42: 'Leg Press Unilateral Left',
    43: 'Leg Press Unilateral Right',
    44: 'Quad-Extension',
    45: 'Quad-Extension Unilateral Left',
    46: 'Quad-Extension Unilateral Right',
    47: 'Hamstring Curl',
    48: 'Hamstring Curl Unilateral Left',
    49: 'Hamstring Curl Unilateral Right',
    50: 'Calf Press',
    51: 'Calf Press Unilateral Left',
    52: 'Calf Press Unilateral Right',
    53: 'Soleus Press'
}

def display_workout_data(client_id):
    # Specify the table and columns to retrieve
    table = 'workouts'
    columns = ['client_id', 'workout_vector', 'time_total', 'workout_status']

    # Specify the condition for matching client_id
    where_columns = ['client_id']
    where_values = [client_id]

    # Retrieve the data from the database
    results = Operations.data_retrieval(table, columns, where_columns, where_values)

    # Create a dictionary to store the workout data
    workout_dict = {}

    # Iterate over the retrieved data
    for row in results:
        workout_vector = row[1]

        # Iterate over each nested list in the workout_vector
        for nested_list in workout_vector:
            # Check if the nested list is a list and has a length of 4
            if isinstance(nested_list, list) and len(nested_list) == 4:
                x, y, z, w = nested_list

                # Check if y, z, and w are numbers
                if isinstance(y, (int, float)) and isinstance(z, (int, float)) and isinstance(w, (int, float)):
                    # Check if x is unique
                    if str(x) not in workout_dict:
                        # Create a new key-value pair for the unique x and evade potential division by zero
                        if w != 0:
                            workout_dict[str(x)] = y * z / w
                            workout_dict[f"{x} number of entries"] = 1
                        else:
                            pass
                    else:
                        # Update the existing key-value pair for the non-unique x
                        workout_dict[str(x)] += y * z * w
                        workout_dict[f"{x} number of entries"] += 1

    # Create a DataFrame from the workout_dict
    if workout_dict:
        df = pd.DataFrame(list(workout_dict.items()), columns=["x", "Average"])
        df["x"] = df["x"].apply(lambda x: int(x) if x.isdigit() else x)
        df = df[df["x"].apply(lambda x: isinstance(x, int))]
        df = df.sort_values(by="x")

        # Replace numeric values in the "x" column with corresponding exercise names
        df["x"] = df["x"].map(exercise_matrix)
    else:
        # If the workout_dict is empty, create an empty DataFrame with the desired columns
        df = pd.DataFrame(columns=["x", "Average"])

    return df


def display_workout_data(client_id):
    # Specify the table and columns to retrieve
    table = 'workouts'
    columns = ['client_id', 'workout_vector', 'time_total', 'workout_status']

    # Specify the condition for matching client_id
    where_columns = ['client_id']
    where_values = [client_id]

    # Retrieve the data from the database
    results = Operations.data_retrieval(table, columns, where_columns, where_values)

    # Create a dictionary to store the workout data
    workout_dict = {}

    # Iterate over the retrieved data
    for row in results:
        workout_vector = row[1]

        # Iterate over each nested list in the workout_vector
        for nested_list in workout_vector:
            # Check if the nested list is a list and has a length of 4
            if isinstance(nested_list, list) and len(nested_list) == 4:
                x, y, z, w = nested_list

                # Check if y, z, and w are numbers
                if isinstance(y, (int, float)) and isinstance(z, (int, float)) and isinstance(w, (int, float)):
                    # Check if x is unique
                    if str(x) not in workout_dict:
                        # Create a new key-value pair for the unique x
                        if w != 0:
                            workout_dict[str(x)] = y * z / w
                            workout_dict[f"{x} number of entries"] = 1
                    else:
                        # Update the existing key-value pair for the non-unique x
                        workout_dict[str(x)] += y * z / w
                        workout_dict[f"{x} number of entries"] += 1

    # Create a DataFrame from the workout_dict
    df = pd.DataFrame(list(workout_dict.items()), columns=["x", "Average"])
    df["x"] = df["x"].apply(lambda x: int(x) if x.isdigit() else x)
    df = df[df["x"].apply(lambda x: isinstance(x, int))]
    df = df.sort_values(by="x")

    # Create a dictionary mapping numeric values to exercise names


    # Replace numeric values in the "x" column with corresponding exercise names
    df["x"] = df["x"].map(exercise_matrix)

    return df

