class Filters:

    @staticmethod
    def to_matrix_translation(exercise, weight, reps, heart_rate=0):
        exercise_matrix = {
            'Shoulder Press': 1,
            'Shoulder Press Unilateral Left': 2,
            'Shoulder Press Unilateral Right': 3,
            'Lateral Raise': 4,
            'Lateral Raise Unilateral Left': 5,
            'Lateral Raise Unilateral Right': 6,
            'Front Raise': 7,
            'Rear Deltoid Fly': 8,
            'Lat Pull-down': 9,
            'Lat Pull-down Inward-Grip': 10,
            'Lat Pull-down Reverse Grip': 11,
            'Lat Pull-down Unilateral Left': 12,
            'Lat Pull-down Unilateral Right': 13,
            'Lat Push-Down': 14,
            'Row': 15,
            'Row Unilateral Left': 16,
            'Row Unilateral Right': 17,
            'Pull-up': 18,
            'Bench Press': 19,
            'Push-up': 20,
            'Dip': 21,
            'Incline Press': 22,
            'Decline Press': 23,
            'Dumbbell Press': 24,
            'Dumbbell Press Unilateral Left': 25,
            'Dumbbell Press Unilateral Right': 26,
            'Pec Fly': 27,
            'Dumbbell Fly': 28,
            'Dumbbell Pec Circle': 29,
            'Bicep Curl': 30,
            'Bicep Curl Unilateral Left': 31,
            'Bicep Curl Unilateral Right': 32,
            'Tricep Extension': 33,
            'Tricep Extension Unilateral Left': 34,
            'Tricep Extension Unilateral Right': 35,
            'Hammer Curl': 36,
            'Squat': 37,
            'Bulgarian Squat': 38,
            'Lunge': 39,
            'Walking Lunge': 40,
            'Leg Press': 41,
            'Leg Press Unilateral Left': 42,
            'Leg Press Unilateral Right': 43,
            'Quad-Extension': 44,
            'Quad-Extension Unilateral Left': 45,
            'Quad-Extension Unilateral Right': 46,
            'Hamstring Curl': 47,
            'Hamstring Curl Unilateral Left': 48,
            'Hamstring Curl Unilateral Right': 49,
            'Calf Press': 50,
            'Calf Press Unilateral Left': 51,
            'Calf Press Unilateral Right': 52,
            'Soleus Press': 53
        }

        exercise_value = exercise_matrix.get(exercise, 0)
        print(f'TO_MATRIX_TRANSLATION\n\tEXERCISE_VALUE : {exercise_value}')
        if exercise_value != 0:
            return [exercise_value, weight, reps, heart_rate]
        else:
            return [0, 0, 0, 0]

    @staticmethod
    def get_exercises():
        exercise_dict = {
            'Shoulders': ['Shoulder Press', 'Shoulder Press Unilateral Left',
                          'Shoulder Press Unilateral Right', 'Lateral Raise',
                          'Lateral Raise Unilateral Left', 'Lateral Raise Unilateral Right',
                          'Front Raise', 'Rear Deltoid Fly'],
            'Back': ['Lat Pull-down', 'Lat Pull-down Inward-Grip', 'Lat Pull-down Reverse Grip',
                     'Lat Pull-down Unilateral Left', 'Lat Pull-down Unilateral Right',
                     'Lat Push-Down', 'Row', 'Row Unilateral Left', 'Row Unilateral Right', 'Pull-up'],
            'Chest': ['Bench Press', 'Push-up', 'Dip', 'Incline Press', 'Decline Press',
                      'Dumbbell Press', 'Dumbbell Press Unilateral Left', 'Dumbbell Press Unilateral Right',
                      'Pec Fly', 'Dumbbell Fly', 'Dumbbell Pec Circle'],
            'Arms': ['Bicep Curl', 'Bicep Curl Unilateral Left', 'Bicep Curl Unilateral Right',
                     'Tricep Extension', 'Tricep Extension Unilateral Left',
                     'Tricep Extension Unilateral Right', 'Hammer Curl'],
            'Legs': ['Squat', 'Bulgarian Squat', 'Lunge', 'Walking Lunge', 'Leg Press',
                     'Leg Press Unilateral Left', 'Leg Press Unilateral Right', 'Quad-Extension',
                     'Quad-Extension Unilateral Left', 'Quad-Extension Unilateral Right',
                     'Hamstring Curl', 'Hamstring Curl Unilateral Left',
                     'Hamstring Curl Unilateral Right', 'Calf Press', 'Calf Press Unilateral Left',
                     'Calf Press Unilateral Right', 'Soleus Press'],
            'Core': ['Crunch', 'Plank', 'Russian Twist']
        }
        return exercise_dict

    @staticmethod
    def matrix_to_english(workout_matrix):
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

        workout_details = []
        for exercise_info in workout_matrix:
            exercise_id = exercise_info[0]
            weight = exercise_info[1]
            reps = exercise_info[2]
            heart_rate = exercise_info[3] if len(exercise_info) > 3 else 0  # Default heart rate to 0 if not present

            exercise_name = exercise_matrix.get(exercise_id, 'Unknown Exercise')
            workout_detail = f"{exercise_name}: {weight} lbs {reps} reps"
            if heart_rate > 0:
                workout_detail += f" (HR: {heart_rate})"
            workout_details.append(workout_detail)

        return '\n'.join(workout_details)

    @staticmethod
    def get_exercise_movements(exercise_id):
        print(f'EXERCISE_ID AFTER FUNCTION CALL : {exercise_id}')
        exercise_movements = {
            1: [1, 3, 'Shoulder Flexion', 'Shoulder Abduction'],
            2: [1, 3, 'Shoulder Flexion', 'Shoulder Abduction'],
            3: [1, 3, 'Shoulder Flexion', 'Shoulder Abduction'],
            4: [3, 'Shoulder Abduction'],
            5: [3, 'Shoulder Abduction'],
            6: [3, 'Shoulder Abduction'],
            7: [1, 'Shoulder Flexion'],
            8: [2, 'Shoulder Extension'],
            9: [4, 'Shoulder Adduction'],
            10: [4, 'Shoulder Adduction'],
            11: [4, 'Shoulder Adduction'],
            12: [4, 'Shoulder Adduction'],
            13: [4, 'Shoulder Adduction'],
            14: [4, 'Shoulder Adduction'],
            15: [4, 'Shoulder Adduction'],
            16: [4, 'Shoulder Adduction'],
            17: [4, 'Shoulder Adduction'],
            18: [4, 'Shoulder Adduction'],
            19: [5, 'Shoulder Horizontal Adduction'],
            20: [5, 'Shoulder Horizontal Adduction'],
            21: [5, 'Shoulder Horizontal Adduction'],
            22: [5, 'Shoulder Horizontal Adduction'],
            23: [5, 'Shoulder Horizontal Adduction'],
            24: [5, 'Shoulder Horizontal Adduction'],
            25: [5, 'Shoulder Horizontal Adduction'],
            26: [5, 'Shoulder Horizontal Adduction'],
            27: [6, 'Shoulder Horizontal Abduction'],
            28: [6, 'Shoulder Horizontal Abduction'],
            29: [6, 5, 'Shoulder Horizontal Abduction', 'Shoulder Horizontal Adduction'],
            30: [7, 8, 'Elbow Flexion', 'Shoulder Internal Rotation'],
            31: [7, 8, 'Elbow Flexion', 'Shoulder Internal Rotation'],
            32: [7, 8, 'Elbow Flexion', 'Shoulder Internal Rotation'],
            33: [9, 10, 'Elbow Extension', 'Shoulder External Rotation'],
            34: [9, 10, 'Elbow Extension', 'Shoulder External Rotation'],
            35: [9, 10, 'Elbow Extension', 'Shoulder External Rotation'],
            36: [7, 8, 'Elbow Flexion', 'Shoulder Internal Rotation'],
            37: [11, 12, 'Hip Flexion', 'Knee Flexion'],
            38: [11, 12, 'Hip Flexion', 'Knee Flexion'],
            39: [11, 12, 'Hip Flexion', 'Knee Flexion'],
            40: [11, 12, 'Hip Flexion', 'Knee Flexion'],
            41: [13, 'Knee Extension'],
            42: [13, 'Knee Extension'],
            43: [13, 'Knee Extension'],
            44: [13, 'Knee Extension'],
            45: [13, 'Knee Extension'],
            46: [13, 'Knee Extension'],
            47: [12, 14, 'Knee Flexion', 'Hip Extension'],
            48: [12, 14, 'Knee Flexion', 'Hip Extension'],
            49: [12, 14, 'Knee Flexion', 'Hip Extension'],
            50: [15, 'Ankle Plantar Flexion'],
            51: [15, 'Ankle Plantar Flexion'],
            52: [15, 'Ankle Plantar Flexion'],
            53: [15, 'Ankle Plantar Flexion']
        }
        print(f'EXERCISE_ID : {exercise_id}')
        if exercise_id in exercise_movements:
            print(f'GET_EXERCISE_MOVEMENT() EXERCISE_ID : {exercise_id}')
            return exercise_movements[exercise_id]
        elif exercise_id == 30:  # Handle "Bicep Curl" exercise
            return [7, 8, 'Elbow Flexion', 'Shoulder Internal Rotation']
        else:
            return []


