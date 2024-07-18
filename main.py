from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import VarFiltering
import CrudOperations
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
import datetime
import time
from kivymd.uix.card import MDCard
from collections import defaultdict
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from CrudOperations import Operations as C
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDRectangleFlatButton
from Calculations import *
import math


V = VarFiltering.Filters
C = CrudOperations.Operations

time_tracing = []
stress_tracing = []


class NewClientScreen(MDScreen):
    def __init__(self, **kwargs):
        """
        Initialize the NewClientScreen.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.name = 'new_client'

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create text fields for Full Name, Date of Birth, and Gender
        self.name_field = MDTextField(hint_text="Full Name")
        self.dob_field = MDTextField(hint_text="Date of Birth (YYYY-MM-DD)")
        self.gender_field = MDTextField(hint_text="Gender")
        self.weight_field = MDTextField(hint_text="Body Weight")

        # Create buttons for Back and Submit
        button_layout = MDBoxLayout(orientation='horizontal', spacing=10)
        back_button = MDRectangleFlatButton(text="Back", on_release=self.go_back)
        submit_button = MDRectangleFlatButton(text="Submit", on_release=self.submit_client)
        button_layout.add_widget(back_button)
        button_layout.add_widget(submit_button)

        main_layout.add_widget(self.name_field)
        main_layout.add_widget(self.dob_field)
        main_layout.add_widget(self.gender_field)
        main_layout.add_widget(self.weight_field)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        """
        Navigate back to the client selection screen.

        Args:
            instance: The instance of the button that triggered the event.
        """
        self.manager.current = 'client_selection'

    def submit_client(self, instance):
        """
        Submit the new client information to the database.

        Args:
            instance: The instance of the button that triggered the event.
        """
        name = self.name_field.text.strip()
        dob = self.dob_field.text.strip()
        gender = self.gender_field.text.strip()
        weight = self.weight_field.text.strip()

        if name and dob and gender:
            # Generate a new client ID
            max_client_id = self.get_max_client_id()
            new_client_id = max_client_id + 1

            # Insert the new client into the database
            client_data = {
                'client_id': new_client_id,
                'client_name': name,
                'gender': gender,
                'dob': dob,
                'weight': float(weight)
            }
            action = 'INSERT'
            table = 'clients'
            columns = list(client_data.keys())
            values = tuple(client_data.values())

            try:
                C.data_adjustment(action, table, columns, values)
            except Exception as e:
                print(f"Error inserting new client: {str(e)}")
                return

            # Clear the text fields
            self.name_field.text = ""
            self.dob_field.text = ""
            self.gender_field.text = ""

            # Navigate back to the client selection screen
            self.manager.current = 'client_selection'
        else:
            print("Please fill in all the required fields.")

    def get_max_client_id(self):
        """
        Get the maximum client ID from the database.

        Returns:
            int: The maximum client ID, or 0 if no clients exist.
        """
        table = 'clients'
        columns = ['MAX(client_id)']

        try:
            result = C.data_retrieval(table, columns)
            max_client_id = result[0][0] if result and result[0][0] is not None else 0
            return max_client_id
        except Exception as e:
            print(f"Error retrieving maximum client ID: {str(e)}")
            return 0


class ClientSelectionScreen(MDScreen):
    def __init__(self, **kwargs):
        """
        Initialize the ClientSelectionScreen.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.name = 'client_selection'
        self.selected_client_id = None
        self.selected_client_name = None
        self.client_select_test_lst = []

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create a layout for the client selection list
        client_selection_layout = MDBoxLayout(orientation='vertical', spacing=10)
        self.client_selection_list = MDList()
        client_selection_scroll = MDScrollView(size_hint=(1, 1))
        client_selection_scroll.add_widget(self.client_selection_list)
        client_selection_layout.add_widget(client_selection_scroll)

        new_client_button = MDRectangleFlatButton(
            text="New Client",
            size_hint=(1, None),
            height=40,
            on_release=self.go_to_new_client
        )
        client_selection_layout.add_widget(new_client_button)

        # Populate the client selection list
        self.load_clients()

        main_layout.add_widget(client_selection_layout)
        self.add_widget(main_layout)

    def go_to_new_client(self, instance):
        """
        Navigate to the new client screen.

        Args:
            instance: The instance of the button that triggered the event.
        """
        self.manager.current = 'new_client'

    def load_clients(self):
        """
        Load the clients from the database and populate the client selection list.
        """
        # Retrieve clients from the database
        table = 'clients'
        columns = ['client_id', 'client_name']
        try:
            clients = C.data_retrieval(table, columns)
        except Exception as e:
            print(f"Error retrieving clients: {str(e)}")
            return

        # Add each client to the selection list
        for client_id, client_name in clients:
            client_button = MDRectangleFlatButton(
                text=client_name,
                size_hint=(1, None),
                height=40,
                on_release=lambda x, id=client_id, name=client_name: self.select_client(id, name)
            )
            self.client_selection_list.add_widget(client_button)

    def select_client(self, client_id, client_name):
        """
        Store the selected client's information and navigate to the main screen.

        Args:
            client_id (int): The ID of the selected client.
            client_name (str): The name of the selected client.
        """
        # Store the selected client's information
        self.selected_client_id = client_id
        self.selected_client_name = client_name
        print(f"Selected Client ID: {self.selected_client_id}")
        print(f"Selected Client Name: {self.selected_client_name}")

        # Pass the selected client's information to the MainScreen
        main_screen = self.manager.get_screen('main')
        main_screen.update_client_info(client_id, client_name)

        # Pass the selected client's information to the WorkoutStartScreen
        workout_start_screen = self.manager.get_screen('workout_start')
        workout_start_screen.client_id = client_id

        self.manager.current = 'main'


class MainScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        """
        Initialize the MainScreen.

        Args:
            client_selection_screen: The instance of the ClientSelectionScreen.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.name = "main"
        self.client_selection_screen = client_selection_screen

        main_layout = MDBoxLayout(orientation='vertical', spacing=40, padding=40)

        debug_layout = MDBoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=10)
        self.debug_label_name = MDLabel(
            text="SELECTED CLIENT: None",
            halign='center',
            valign='center',
            size_hint=(1, 1)
        )
        self.debug_label_id = MDLabel(
            text="CLIENT ID: None",
            halign='center',
            valign='center',
            size_hint=(1, 1)
        )

        button_layout = MDBoxLayout(orientation='vertical', spacing=20, size_hint=(0.5, 0.6))
        buttons = ['Start Workout', 'Workout Design', 'Goals', 'Progress', 'Testing', 'Documents / Notes']
        for button_text in buttons:
            button = MDRectangleFlatButton(
                text=button_text,
                size_hint=(1, None),
                height=60,
                on_release=self.navigate_to_screen
            )
            button_layout.add_widget(button)

        user_profile_layout = MDBoxLayout(orientation='vertical', spacing=20, size_hint=(0.5, 0.6))
        self.user_info = [
            {'label': 'Client Selected', 'value': 'None'},
            {'label': 'User ID', 'value': 'None'}
        ]
        self.user_info_labels = []
        for info in self.user_info:
            label = MDLabel(
                text=f"{info['label']}: {info['value']}",
                halign='left',
                valign='top',
                size_hint_y=None,
                height=60
            )
            self.user_info_labels.append(label)
            user_profile_layout.add_widget(label)

        main_layout.add_widget(debug_layout)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(user_profile_layout)

        self.add_widget(main_layout)

    def update_client_info(self, client_id, client_name):
        """
        Update the client information displayed on the main screen.

        Args:
            client_id (int): The ID of the selected client.
            client_name (str): The name of the selected client.
        """
        self.selected_client_id = client_id
        self.selected_client_name = client_name
        self.debug_label_name.text = f"SELECTED CLIENT: {client_name}"
        self.debug_label_id.text = f"CLIENT ID: {client_id}"
        self.user_info[0]['value'] = client_name
        self.user_info[1]['value'] = client_id
        self.user_info_labels[0].text = f"Name: {client_name}"
        self.user_info_labels[1].text = f"User ID: {client_id}"

    def navigate_to_screen(self, instance):
        """
        Navigate to the corresponding screen based on the button clicked.

        Args:
            instance: The instance of the button that triggered the event.
        """
        screen_name = instance.text.lower().replace(' ', '_')
        if screen_name == 'workout_design':
            workout_design_screen = self.manager.get_screen('workout_design')
            workout_design_screen.client_id = self.selected_client_id
            self.manager.current = screen_name
        elif screen_name == 'start_workout':
            self.manager.current = 'workout_start'
        elif screen_name == 'goals':
            self.manager.current = screen_name
        elif screen_name == 'documents_/_notes':
            self.manager.current = 'documents_notes'
        elif screen_name == 'progress':
            self.manager.current = screen_name
        elif screen_name == 'testing':
            self.manager.current = 'testing'
        else:
            print(f"Screen '{screen_name}' is not implemented yet.")


class WorkoutPlannerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "700"

        self.screen_manager = ScreenManager()
        self.client_selection_screen = ClientSelectionScreen(name='client_selection')
        self.screen_manager.add_widget(self.client_selection_screen)

        self.main_screen = MainScreen(client_selection_screen=self.client_selection_screen, name='main')
        self.screen_manager.add_widget(self.main_screen)


        self.new_client_screen = NewClientScreen(name='new_client')
        self.screen_manager.add_widget(self.new_client_screen)

        self.screen_manager.add_widget(WorkoutDesignScreen(client_selection_screen=self.client_selection_screen, name='workout_design'))

        self.screen_manager.add_widget(WorkoutStartScreen(client_selection_screen=self.client_selection_screen, name='workout_start'))
        self.screen_manager.add_widget(GoalsScreen(client_selection_screen=self.client_selection_screen, name='goals'))
        self.screen_manager.add_widget(ProgressScreen(client_selection_screen=self.client_selection_screen, name='progress'))
        self.screen_manager.add_widget(
            TestingScreen(client_selection_screen=self.client_selection_screen, name='testing'))
        self.screen_manager.add_widget(DocumentsNotesScreen(client_selection_screen=self.client_selection_screen, name='documents_notes'))
        self.screen_manager.add_widget(WorkoutDetailsScreen(client_selection_screen=self.client_selection_screen,
                                                            client_id=self.client_selection_screen.selected_client_id,
                                                            name='workout_details'))
        self.screen_manager.add_widget(
            BioMetricsScreen(client_selection_screen=self.client_selection_screen, name='biometrics'))
        self.screen_manager.add_widget(WorkoutSummaryScreen(client_id=self.client_selection_screen.selected_client_id, name='workout_summary'))

        return self.screen_manager


class WorkoutStartScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'workout_start'
        self.client_selection_screen = client_selection_screen
        self.client_id = None
        self.exercise_start_time = None

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Add a back button at the top
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back,
            pos_hint={'left': 1, 'top': 1}
        )
        main_layout.add_widget(back_button)

        content_layout = MDBoxLayout(orientation='horizontal', spacing=20)

        start_new_workout_button = MDRectangleFlatButton(
            text="Design Workout",
            size_hint=(0.3, None),
            height=60,
            on_release=self.start_new_workout
        )

        previous_workouts_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint=(0.7, 1))
        previous_workouts_scroll = MDScrollView(size_hint=(1, 1))
        self.previous_workouts_list = MDList()

        previous_workouts_scroll.add_widget(self.previous_workouts_list)
        previous_workouts_layout.add_widget(previous_workouts_scroll)

        content_layout.add_widget(start_new_workout_button)
        content_layout.add_widget(previous_workouts_layout)

        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        # Navigate back to the main screen
        self.manager.current = 'main'

    def on_pre_enter(self, *args):
        self.client_id = self.client_selection_screen.selected_client_id
        print(f"WorkoutStartScreen - Client ID: {self.client_id}")
        self.get_previous_workouts()

    def start_new_workout(self, instance):
        # Navigate to the workout design screen to start a new workout
        self.manager.current = 'workout_design'

    def get_previous_workouts(self):
        # Retrieve previous workouts from the database
        print(f'CURRENT CLIENT ID: {self.client_id}')
        table = 'workouts'
        columns = ['workouts_id', 'client_id', 'workout_vector', 'workout_date', 'wo_type']
        where_columns = ['client_id']
        where_values = [self.client_id]
        order_by = 'workout_date DESC'

        previous_workouts = C.data_retrieval(table, columns, where_columns=where_columns, where_values=where_values,
                                             order_by=order_by)

        # Clear the previous workouts list
        self.previous_workouts_list.clear_widgets()

        # Add the previous workouts to the list
        for workout in previous_workouts:
            workout_button = MDRectangleFlatButton(
                text=f"{workout[4]} - {workout[3]}",
                size_hint=(1, None),
                height=40,
                on_release=lambda x, workout_id=workout[0]: self.load_previous_workout(workout_id)
            )
            self.previous_workouts_list.add_widget(workout_button)

    def load_previous_workout(self, workout_id):
        # Navigate to the workout details screen and load the workout details
        workout_details_screen = self.manager.get_screen('workout_details')
        workout_details_screen.load_workout_details(workout_id)
        self.manager.current = 'workout_details'


class WorkoutDesignScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = "workout_design"
        self.client_selection_screen = client_selection_screen
        self.client_id = None

        self.workout_vector = []
        self.exercise_list = []
        self.live_workout_list = MDList()

        self.current_exercise = None
        self.current_weight = ""
        self.current_reps = ""

        self.d_force_shoulders = []
        self.d_force_pull = []
        self.d_force_push = []
        self.d_force_arms = []
        self.d_force_legs = []
        self.d_force_core = []

        main_layout = MDBoxLayout(orientation='horizontal', spacing=20, padding=20)

        input_layout = MDBoxLayout(orientation='vertical', spacing=20, size_hint_x=0.6)

        muscle_group_layout = MDBoxLayout(orientation='vertical', spacing=10)
        muscle_groups = ['Shoulders', 'Back', 'Chest', 'Arms', 'Legs']
        for muscle_group in muscle_groups:
            muscle_group_button = MDFlatButton(
                text=muscle_group,
                on_release=self.show_exercise_list
            )
            muscle_group_layout.add_widget(muscle_group_button)

        self.weight_field = MDTextField(
            hint_text="Weight",
            helper_text="Enter the weight in lbs",
            helper_text_mode="on_focus",
            size_hint_x=0.5
        )

        self.reps_field = MDTextField(
            hint_text="Reps",
            helper_text="Enter the number of reps",
            helper_text_mode="on_focus",
            size_hint_x=0.5
        )

        self.add_exercise_button = MDFlatButton(
            text="Add Exercise",
            on_release=self.add_exercise
        )

        self.complete_button = MDFlatButton(
            text="Complete",
            on_release=self.complete_workout
        )

        input_layout.add_widget(muscle_group_layout)
        input_layout.add_widget(self.weight_field)
        input_layout.add_widget(self.reps_field)
        input_layout.add_widget(self.add_exercise_button)
        input_layout.add_widget(self.complete_button)

        list_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint_x=0.4)

        self.exercise_scroll = MDScrollView()
        self.exercise_box = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=10,
            padding=10
        )
        self.exercise_scroll.add_widget(self.exercise_box)

        # Replace the selected exercise list with a label
        self.selected_exercise_label = MDLabel(
            text="No exercise selected",
            size_hint=(1, None),
            height=50,
            halign="center"
        )

        self.added_exercises_scroll = MDScrollView()
        self.added_exercises_list = MDList()
        self.added_exercises_scroll.add_widget(self.added_exercises_list)

        list_layout.add_widget(self.exercise_scroll)
        list_layout.add_widget(self.selected_exercise_label)
        list_layout.add_widget(self.added_exercises_scroll)

        main_layout.add_widget(input_layout)
        main_layout.add_widget(list_layout)

        self.add_widget(main_layout)

    def on_pre_enter(self, *args):
        self.client_id = self.client_selection_screen.selected_client_id
        print(f"WorkoutDesignScreen - Client ID: {self.client_id}")

    def show_exercise_list(self, instance):
        muscle_group = instance.text
        exercises = self.get_exercises(muscle_group)
        self.exercise_box.clear_widgets()
        for exercise in exercises:
            self.exercise_box.add_widget(
                OneLineListItem(
                    text=exercise,
                    on_release=lambda x, exercise=exercise: self.select_exercise(exercise)
                )
            )

    def get_exercises(self, muscle_group):
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
        return exercise_dict.get(muscle_group, [])

    def select_exercise(self, exercise_name):
        self.current_exercise = exercise_name
        self.selected_exercise_label.text = f"Selected: {exercise_name}"

    def add_exercise(self, instance):
        weight_text = self.weight_field.text.strip()
        reps_text = self.reps_field.text.strip()

        if weight_text and reps_text:
            try:
                weight = int(weight_text)
                reps = int(reps_text)
            except ValueError:
                # Clear the weight and reps fields without taking any action
                self.weight_field.text = ""
                self.reps_field.text = ""
                return

            updated_details = f"{self.current_exercise}: {weight} lbs {reps} reps"

            # Add the exercise to the live workout list at the top
            live_workout_item = OneLineListItem(text=updated_details)
            self.live_workout_list.add_widget(live_workout_item, index=0)

            # Add the exercise to the added exercises list
            added_exercise_item = OneLineListItem(text=updated_details)
            self.added_exercises_list.add_widget(added_exercise_item, index=0)

            # Add the exercise to the new workout vector
            exercise_info = V.to_matrix_translation(self.current_exercise, weight, reps, 0)
            self.workout_vector.append(exercise_info)

            # Clear the weight and reps fields
            self.weight_field.text = ""
            self.reps_field.text = ""
        else:
            # Clear the weight and reps fields without taking any action
            self.weight_field.text = ""
            self.reps_field.text = ""

    def det_workout(self, vector):
        # Initialize force distribution lists
        d_force_shoulders = []
        d_force_pull = []
        d_force_push = []
        d_force_arms = []
        d_force_legs = []
        d_force_core = []

        # Iterate over the workout vector
        for exercise_info in vector:
            exercise_id, weight, reps, _ = exercise_info  # Unpack exercise_info with an underscore for heart_rate
            stress = weight * reps

            if exercise_id >= 1 and exercise_id <= 8:
                d_force_shoulders.append(stress)
            elif exercise_id >= 9 and exercise_id <= 18:
                d_force_pull.append(stress)
            elif exercise_id >= 19 and exercise_id <= 29:
                d_force_push.append(stress)
            elif exercise_id >= 30 and exercise_id <= 36:
                d_force_arms.append(stress)
            elif exercise_id >= 37 and exercise_id <= 53:
                d_force_legs.append(stress)
            else:
                d_force_core.append(stress)

        # Calculate total stress for each muscle group
        total_shoulders = sum(d_force_shoulders)
        total_pull = sum(d_force_pull)
        total_push = sum(d_force_push)
        total_arms = sum(d_force_arms)
        total_legs = sum(d_force_legs)
        total_core = sum(d_force_core)

        # Calculate total stress for the entire workout
        total_stress = total_shoulders + total_pull + total_push + total_arms + total_legs + total_core

        # Determine the percentage distribution of each muscle group
        if total_stress != 0:
            percent_shoulders = (total_shoulders / total_stress) * 100
            percent_pull = (total_pull / total_stress) * 100
            percent_push = (total_push / total_stress) * 100
            percent_arms = (total_arms / total_stress) * 100
            percent_legs = (total_legs / total_stress) * 100
            percent_core = (total_core / total_stress) * 100
        else:
            percent_shoulders = percent_pull = percent_push = percent_arms = percent_legs = percent_core = 0

        # Determine the muscle group with the highest percentage
        muscle_percentages = {
            'Shoulders': percent_shoulders,
            'Pull': percent_pull,
            'Push': percent_push,
            'Arms': percent_arms,
            'Legs': percent_legs,
            'Core': percent_core
        }
        max_muscle_group = max(muscle_percentages, key=muscle_percentages.get)

        return f"{max_muscle_group} Day"

    def update_workout_vector_in_database(self):
        # Get the current date
        current_date = datetime.date.today()

        # Prepare the workout data
        workout_data = {
            'client_id': self.client_id,
            'workout_vector': self.workout_vector,
            'workout_date': current_date,
            'wo_type': self.det_workout(self.workout_vector),  # Set the workout type based on the force distribution
            'workout_status': 'In Progress'  # Set the workout status
        }

        # Update the workout vector in the database
        action = 'UPDATE'
        table = 'workouts'
        columns = ['workout_vector', 'wo_type', 'workout_status']  # Include 'wo_type' and 'workout_status' columns
        values = [self.workout_vector, workout_data['wo_type'], workout_data['workout_status']]
        where_columns = ['client_id', 'workout_date']
        where_values = [workout_data['client_id'], workout_data['workout_date']]

        C.data_adjustment(action, table, columns, values, where_columns, where_values)

    def complete_workout(self, instance):
        if not self.workout_vector:
            # If the workout vector is empty, navigate back to the main screen without adding to the database
            self.manager.current = 'main'
            return

        # Get the current date
        current_date = datetime.date.today()

        # Determine the workout type based on force distribution
        wo_type = self.det_workout(self.workout_vector)

        # Prepare the workout data
        workout_data = {
            'client_id': self.client_id,
            'workout_vector': self.workout_vector,
            'workout_date': current_date,
            'wo_type': wo_type,
            'workout_status': 'Not Completed'  # Set the workout status as 'Not Completed'
        }

        # Insert the workout data into the database
        action = 'INSERT'
        table = 'workouts'
        columns = list(workout_data.keys())
        values = tuple(workout_data.values())

        C.data_adjustment(action, table, columns, values)

        # Clear the workout data and update the UI
        self.workout_vector = []
        self.exercise_list = []
        self.selected_exercise_label.text = "No exercise selected"
        self.added_exercises_list.clear_widgets()

        # Navigate back to the main screen
        self.manager.current = 'main'


class ExerciseCompletePopup(Popup):
    def __init__(self, exercise, weight, rep, h_rate, duration, on_dismiss_callback, on_cancel_callback, client_selection_screen, exercise_duration, **kwargs):
        super(ExerciseCompletePopup, self).__init__(**kwargs)
        self.title = exercise
        self.size_hint = (0.6, 0.6)
        self.exercise = exercise
        self.weight = weight
        self.rep = rep
        self.h_rate = h_rate
        self.duration = duration
        self.on_dismiss_callback = on_dismiss_callback
        self.on_cancel_callback = on_cancel_callback
        self.client_selection_screen = client_selection_screen
        self.exercise_duration = exercise_duration  # Assign the exercise_duration to an instance variable

        main_layout = BoxLayout(orientation='vertical', padding=10)

        # Add a cancel button at the top left
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        cancel_button = MDFlatButton(
            text="Cancel",
            on_release=self.on_cancel,
            pos_hint={'left': 1, 'top': 1}
        )
        top_layout.add_widget(cancel_button)
        top_layout.add_widget(Widget())  # This empty widget will push the cancel button to the left

        main_layout.add_widget(top_layout)

        label = Label(text=f"Weight: {self.weight}           Heart Rate: {self.h_rate}\n\nRepetition: {self.rep}",
                      font_size=33)
        info_label = Label(text=self.review_text(), font_size=25)

        muscle_group = self.get_muscle_group(exercise)
        metabolic_efficiency = self.calculate_metabolic_efficiency(muscle_group)
        metabolic_efficiency_label = Label(text=metabolic_efficiency, font_size=20, color=(1, 0, 0, 1) if "Unavailable" in metabolic_efficiency else (1, 1, 1, 1))

        close_button = Button(text=f"Confirm {self.exercise}", size_hint=(1, 0.5))
        close_button.bind(on_press=self.on_close)

        main_layout.add_widget(label)
        main_layout.add_widget(info_label)
        main_layout.add_widget(metabolic_efficiency_label)
        main_layout.add_widget(close_button)
        self.content = main_layout

    def on_close(self, instance):
        self.dismiss()
        if self.on_dismiss_callback:
            self.on_dismiss_callback()

    def on_cancel(self, instance):
        self.dismiss()
        if self.on_cancel_callback:
            self.on_cancel_callback()

    def review_text(self) -> str:
        if len(time_tracing) > 1 and len(stress_tracing) > 0:
            total_time = time_tracing[-1] - time_tracing[0]
            total_stress = sum(stress_tracing)
            force_level = total_stress / total_time if total_time > 0 else 0
            return f'Currently: {total_time:.2f} seconds    Force Level: {force_level:.2f} Lbs/T'
        else:
            return 'Workout just started'

    def get_muscle_group(self, exercise):
        exercise_id = V.to_matrix_translation(exercise, 0, 0, 0)[0]
        exercise_movements = V.get_exercise_movements(exercise_id)
        if exercise_movements:
            return exercise_movements[-1]  # Return the last element as the muscle group
        else:
            return "Unknown"

    def calculate_metabolic_efficiency(self, muscle_group):
        client_id = self.client_selection_screen.selected_client_id

        # Retrieve the necessary measurements from the database
        table = 'clients'
        columns = ['vt1', 'heart_rate_descent']
        where_columns = ['client_id']
        where_values = [client_id]

        measurements = C.data_retrieval(table, columns, where_columns, where_values)

        if measurements:
            vt1, heart_rate_descent = measurements[0]

            # Check if all measurements are available
            if all(value is not None for value in measurements[0]):
                weight = self.weight
                reps_per_min = self.rep

                # Retrieve muscle-specific measurements from the database based on the muscle group
                table = 'clients'
                columns = ['neck_mes', 'chest_mes', 'left_arm_mes', 'left_forearm_mes', 'right_arm_mes',
                           'right_forearm_mes', 'waist_mes', 'hips_mes', 'left_thigh_mes', 'right_thigh_mes',
                           'left_calf_mes', 'right_calf_mes']
                where_columns = ['client_id']
                where_values = [client_id]

                muscle_measurements = C.data_retrieval(table, columns, where_columns, where_values)

                if muscle_measurements:
                    muscle_measurements = muscle_measurements[0]
                    muscle_mapping = {
                        'Shoulder Flexion': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Abduction': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Extension': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Adduction': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Horizontal Adduction': ['chest_mes'],
                        'Shoulder Horizontal Abduction': ['chest_mes'],
                        'Elbow Flexion': ['left_forearm_mes', 'right_forearm_mes'],
                        'Shoulder Internal Rotation': ['left_arm_mes', 'right_arm_mes'],
                        'Elbow Extension': ['left_forearm_mes', 'right_forearm_mes'],
                        'Shoulder External Rotation': ['left_arm_mes', 'right_arm_mes'],
                        'Hip Flexion': ['hips_mes'],
                        'Knee Flexion': ['left_thigh_mes', 'right_thigh_mes'],
                        'Knee Extension': ['left_thigh_mes', 'right_thigh_mes'],
                        'Hip Extension': ['hips_mes'],
                        'Ankle Plantar Flexion': ['left_calf_mes', 'right_calf_mes']
                    }

                    circumference_columns = muscle_mapping.get(muscle_group, [])
                    if circumference_columns:
                        circumference = sum(muscle_measurements[columns.index(col)] for col in circumference_columns if
                                            muscle_measurements[columns.index(col)] is not None)
                        length = 10  # Assume a default length of 10 units
                        muscle_density = 1.06  # Assume a muscle density of 1.06 g/cm^3

                        # Calculate the adjusted mechanical efficiency (Madj)
                        weight_reps_per_min = weight * reps_per_min
                        geometric_muscle_factor = (float(circumference) ** 2 * length) / (4 * math.pi)
                        vt1_max_hr_ratio = int(vt1) / self.h_rate
                        max_hr_descent_ratio = self.h_rate / heart_rate_descent

                        time_sec = self.exercise_duration  # Use exercise duration in seconds
                        if time_sec > 0:
                            madj = (
                                               weight_reps_per_min * geometric_muscle_factor * vt1_max_hr_ratio * muscle_density * max_hr_descent_ratio) / time_sec
                            return f"Metabolic Efficiency : {madj:.2f}"  # Return the metabolic efficiency as a string with two decimal places
                        else:
                            return "Unavailable"  # Return "Unavailable" if time_sec is 0 to avoid division by zero
                    else:
                        return "Unavailable"  # Return "Unavailable" if no circumference columns found for the muscle group
                else:
                    return "Unavailable"  # Return "Unavailable" if no muscle measurements found
            else:
                return "Unavailable"  # Return "Unavailable" if not all measurements are available
        else:
            return "Unavailable"  # Return "Unavailable" if no measurements found for the client


class WorkoutDetailsScreen(Screen):
    def __init__(self, client_selection_screen, client_id, **kwargs):
        super().__init__(**kwargs)
        self.name = 'workout_details'
        self.client_selection_screen = client_selection_screen
        self.client_id = client_id
        self.workout_id = None
        self.original_workout_vector = []
        self.metabolic_evaluation = []
        self.new_workout_vector = []
        self.selected_exercise_index = None
        self.selected_exercise_name = None
        self.exercise_times = []
        self.workout_start_time = None
        self.workout_end_time = None
        self.exercise_start_time = None
        self.exercise_duration = 0
        self.weight = None
        self.rep = None
        self.h_rate = 0

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create a layout for the "Back" button and "End Workout" button
        top_button_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back,
            pos_hint={'left': 1}  # Position the "Back" button on the left
        )
        end_workout_button = MDRectangleFlatButton(
            text="End Workout",
            on_release=self.end_workout,
            pos_hint={'right': 1}  # Position the "End Workout" button on the right
        )
        self.start_exercise_button = MDRectangleFlatButton(
            text="Start Exercise",
            size_hint=(1, None),
            height=40,
            on_release=self.start_exercise
        )
        top_button_layout.add_widget(back_button)
        top_button_layout.add_widget(end_workout_button)

        # Create a layout for the workout details lists
        workout_lists_layout = MDBoxLayout(orientation='horizontal', size_hint_y=0.6)

        # Create a scroll view for the workout details from the database
        original_workout_scroll = ScrollView(size_hint_x=0.3)
        self.original_workout_list = MDList()
        original_workout_scroll.add_widget(self.original_workout_list)

        # Create a scroll view for the additional exercise list
        additional_exercise_scroll = ScrollView(size_hint_x=0.4)
        self.additional_exercise_list = MDList()
        additional_exercise_scroll.add_widget(self.additional_exercise_list)

        # Create a scroll view for the workout details during the live session
        live_workout_scroll = ScrollView(size_hint_x=0.3)
        self.live_workout_list = MDList()
        live_workout_scroll.add_widget(self.live_workout_list)

        workout_lists_layout.add_widget(original_workout_scroll)
        workout_lists_layout.add_widget(additional_exercise_scroll)
        workout_lists_layout.add_widget(live_workout_scroll)

        # Create a layout for updating weight, reps, and heart rate
        update_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=140)
        self.weight_field = MDTextField(
            hint_text="Weight",
            size_hint=(1, None),
            height=40
        )
        self.reps_field = MDTextField(
            hint_text="Reps",
            size_hint=(1, None),
            height=40
        )
        self.heart_rate_field = MDTextField(
            hint_text="Heart Rate",
            size_hint=(1, None),
            height=40
        )
        update_button = MDRectangleFlatButton(
            text="Update",
            size_hint=(1, None),
            height=40,
            on_release=self.handle_update_button
        )
        update_layout.add_widget(self.weight_field)
        update_layout.add_widget(self.reps_field)
        update_layout.add_widget(self.heart_rate_field)
        update_layout.add_widget(update_button)

        main_layout.add_widget(self.start_exercise_button)
        main_layout.add_widget(top_button_layout)
        main_layout.add_widget(workout_lists_layout)
        main_layout.add_widget(update_layout)

        self.add_widget(main_layout)

    def calculate_metabolic_efficiency(self, muscle_group):
        """
        Calculate the metabolic efficiency for a given muscle group.

        Args:
            muscle_group (str): The muscle group for which to calculate the metabolic efficiency.

        Returns:
            str: The calculated metabolic efficiency as a string, or "Unavailable" if the calculation is not possible.
        """
        client_id = self.client_selection_screen.selected_client_id

        # Retrieve the necessary measurements from the database
        table = 'clients'
        columns = ['vt1', 'heart_rate_descent']
        where_columns = ['client_id']
        where_values = [client_id]

        measurements = C.data_retrieval(table, columns, where_columns, where_values)

        if measurements:
            vt1, heart_rate_descent = measurements[0]

            # Check if all measurements are available
            if all(value is not None for value in measurements[0]):
                weight = self.weight
                reps_per_min = self.rep

                # Retrieve muscle-specific measurements from the database based on the muscle group
                table = 'clients'
                columns = ['neck_mes', 'chest_mes', 'left_arm_mes', 'left_forearm_mes', 'right_arm_mes',
                           'right_forearm_mes', 'waist_mes', 'hips_mes', 'left_thigh_mes', 'right_thigh_mes',
                           'left_calf_mes', 'right_calf_mes']
                where_columns = ['client_id']
                where_values = [client_id]

                muscle_measurements = C.data_retrieval(table, columns, where_columns, where_values)

                if muscle_measurements:
                    muscle_measurements = muscle_measurements[0]
                    muscle_mapping = {
                        'Shoulder Flexion': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Abduction': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Extension': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Adduction': ['left_arm_mes', 'right_arm_mes'],
                        'Shoulder Horizontal Adduction': ['chest_mes'],
                        'Shoulder Horizontal Abduction': ['chest_mes'],
                        'Elbow Flexion': ['left_forearm_mes', 'right_forearm_mes'],
                        'Shoulder Internal Rotation': ['left_arm_mes', 'right_arm_mes'],
                        'Elbow Extension': ['left_forearm_mes', 'right_forearm_mes'],
                        'Shoulder External Rotation': ['left_arm_mes', 'right_arm_mes'],
                        'Hip Flexion': ['hips_mes'],
                        'Knee Flexion': ['left_thigh_mes', 'right_thigh_mes'],
                        'Knee Extension': ['left_thigh_mes', 'right_thigh_mes'],
                        'Hip Extension': ['hips_mes'],
                        'Ankle Plantar Flexion': ['left_calf_mes', 'right_calf_mes']
                    }

                    circumference_columns = muscle_mapping.get(muscle_group, [])
                    if circumference_columns:
                        circumference = sum(muscle_measurements[columns.index(col)] for col in circumference_columns if
                                            muscle_measurements[columns.index(col)] is not None)
                        length = 10  # Assume a default length of 10 units
                        muscle_density = 1.06  # Assume a muscle density of 1.06 g/cm^3
                        # Calculate the adjusted mechanical efficiency (Madj)
                        weight_reps_per_min = int(weight) * int(reps_per_min)
                        geometric_muscle_factor = (float(circumference) ** 2 * length) / (4 * math.pi)
                        vt1_max_hr_ratio = int(vt1) / int(self.h_rate)
                        max_hr_descent_ratio = int(self.h_rate) / heart_rate_descent

                        time_sec = self.exercise_duration  # Use exercise duration in seconds
                        if time_sec > 0:
                            madj = (
                                               weight_reps_per_min * geometric_muscle_factor * vt1_max_hr_ratio * muscle_density * max_hr_descent_ratio) / time_sec
                            return f"{madj:.2f}"  # Return the metabolic efficiency as a string with two decimal places
                        else:
                            return "Unavailable"  # Return "Unavailable" if time_sec is 0 to avoid division by zero
                    else:
                        return "Unavailable"  # Return "Unavailable" if no circumference columns found for the muscle group
                else:
                    return "Unavailable"  # Return "Unavailable" if no muscle measurements found
            else:
                return "Unavailable"  # Return "Unavailable" if not all measurements are available
        else:
            return "Unavailable"  # Return "Unavailable" if no measurements found for the client

    def get_muscle_group(self, exercise):
        """
        Get the muscle group for a given exercise.

        Args:
            exercise (str): The name of the exercise.

        Returns:
            str: The muscle group associated with the exercise, or "Unknown" if not found.
        """
        exercise_id = V.to_matrix_translation(exercise, 0, 0, 0)[0]
        exercise_movements = V.get_exercise_movements(exercise_id)
        if exercise_movements:
            return exercise_movements[-1]  # Return the last element as the muscle group
        else:
            return "Unknown"

    def start_exercise(self, instance):
        """
        Start the selected exercise by showing a countdown popup.

        Args:
            instance: The instance of the button that triggered the event.
        """
        if self.selected_exercise_name:
            self.show_countdown_popup(self.selected_exercise_name)
        else:
            print("No exercise selected.")

    def show_countdown_popup(self, exercise_name):
        """
        Show a countdown popup before starting the exercise.

        Args:
            exercise_name (str): The name of the exercise to start.
        """
        def update_countdown(dt):
            nonlocal remaining_time
            remaining_time -= 1
            label.text = str(remaining_time)
            if remaining_time <= 0:
                label.text = f"Begin {exercise_name}"
                self.exercise_start_time = time.time()  # Record the exercise start time
                complete_button.disabled = False  # Enable the "Complete" button
                Clock.unschedule(update_countdown)  # Stop the countdown

        def complete_exercise(instance, popup):
            self.exercise_end_time = time.time()
            if self.exercise_start_time is not None:
                self.exercise_duration = 0
                print(f'ou912 ex dur before exercise : {self.exercise_duration}')
                self.exercise_duration = self.exercise_end_time - self.exercise_start_time
                print(f"Time under tension for {exercise_name}: {self.exercise_duration:.2f} seconds")
                print(f'ou912 ex dur AFTER exercise: {self.exercise_duration}')
                self.update_exercise_duration_label(exercise_name, self.exercise_duration)

            else:
                print("Exercise start time not recorded.")
            popup.dismiss()  # Close the popup

        countdown_duration = 2  # Countdown duration in seconds
        remaining_time = countdown_duration
        content = BoxLayout(orientation='vertical')
        label = Label(text=str(countdown_duration))
        popup = Popup(title="Countdown", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        complete_button = Button(text="Complete", size_hint=(1, 0.5),
                                 on_release=lambda instance: complete_exercise(instance, popup), disabled=True)
        content.add_widget(label)
        content.add_widget(complete_button)
        popup.open()
        Clock.schedule_interval(update_countdown, 1)  # Schedule the countdown at 1-second intervals

    def show_exercise_complete_popup(self, exercise, weight, reps, heart_rate):
        """
        Show a popup to confirm the completion of an exercise.

        Args:
            exercise (str): The name of the exercise.
            weight (int): The weight used in the exercise.
            reps (int): The number of repetitions performed.
            heart_rate (int): The heart rate during the exercise.
        """
        popup = ExerciseCompletePopup(
            exercise,
            weight,
            reps,
            heart_rate,
            self.exercise_duration,
            on_dismiss_callback=lambda: self.update_exercise(exercise, weight, reps, heart_rate),
            on_cancel_callback=self.on_cancel_exercise,
            client_selection_screen=self.client_selection_screen,
            exercise_duration=self.exercise_duration  # Pass the exercise_duration attribute
        )
        popup.open()

    def on_cancel_exercise(self):
        """
        Callback function when the exercise is cancelled.
        """
        print("Exercise cancelled")
        self.weight_field.text = ""
        self.reps_field.text = ""
        self.heart_rate_field.text = ""

    def handle_update_button(self, instance):
        """
        Handle the update button press event.

        Args:
            instance: The instance of the button that triggered the event.
        """
        weight_text = self.weight_field.text.strip()
        reps_text = self.reps_field.text.strip()
        heart_rate_text = self.heart_rate_field.text.strip()

        self.weight = weight_text
        self.rep = reps_text
        self.h_rate = heart_rate_text

        if weight_text and reps_text and heart_rate_text:
            try:
                weight = int(weight_text)
                reps = int(reps_text)
                heart_rate = int(heart_rate_text)

                if self.selected_exercise_name:
                    self.show_exercise_complete_popup(self.selected_exercise_name, weight, reps, heart_rate)
                else:
                    print("No exercise selected.")
            except ValueError:
                print("Invalid input. Please enter integers for weight, reps, and heart rate.")
        else:
            print("Please enter weight, reps, and heart rate.")

# ... (previous code remains the same)

    def go_back(self, instance):
        """
        Navigate back to the workout start screen.

        Args:
            instance: The instance of the button that triggered the event.
        """
        time_tracing.clear()
        stress_tracing.clear()
        self.manager.current = 'workout_start'

    def load_workout_details(self, workout_id):
        """
        Load the workout details based on the provided workout ID.

        Args:
            workout_id (int): The ID of the workout to load.
        """
        self.workout_id = workout_id
        self.workout_start_time = time.time()  # Record the workout start time

        # Retrieve the workout details from the database based on the workout_id
        table = 'workouts'
        columns = ['workout_vector']
        where_columns = ['workouts_id']
        where_values = [workout_id]

        workout_data = C.data_retrieval(table, columns, where_columns=where_columns, where_values=where_values)

        if workout_data:
            self.original_workout_vector = workout_data[0][0]  # Store the original workout vector

            # Clear the previous workout details
            self.original_workout_list.clear_widgets()
            self.additional_exercise_list.clear_widgets()
            self.live_workout_list.clear_widgets()

            # Populate the original workout details list
            workout_details = V.matrix_to_english(self.original_workout_vector).split('\n')
            for detail in workout_details:
                workout_detail_item = OneLineListItem(
                    text=detail,
                    on_release=lambda x, text=detail: self.select_exercise(text, from_original_list=True)
                )
                self.original_workout_list.add_widget(workout_detail_item)

            # Populate the additional exercise list with the remaining exercises
            all_exercises = []
            for exercises in V.get_exercises().values():
                all_exercises.extend(exercises)

            remaining_exercises = [exercise for exercise in all_exercises if exercise not in workout_details]
            for exercise in remaining_exercises:
                exercise_item = OneLineListItem(
                    text=exercise,
                    on_release=lambda x, exercise=exercise: self.select_exercise(exercise, from_original_list=False)
                )
                self.additional_exercise_list.add_widget(exercise_item)

        else:
            print(f"No workout found with ID: {workout_id}")

    def update_exercise_duration_label(self, exercise_name, duration):
        """
        Update the exercise duration label for the given exercise.

        Args:
            exercise_name (str): The name of the exercise.
            duration (float): The duration of the exercise in seconds.
        """
        for child in self.live_workout_list.children:
            if child.text.split(':')[0].strip() == exercise_name:
                child.secondary_text = f"Duration: {duration:.2f} seconds"
                break

    def select_exercise(self, exercise_name, from_original_list):
        """
        Select an exercise from either the original workout list or the additional exercise list.

        Args:
            exercise_name (str): The name of the exercise to select.
            from_original_list (bool): True if selecting from the original workout list, False otherwise.
        """
        self.selected_exercise_name = exercise_name.split(':')[0].strip()

        # Deselect the previously selected exercise
        if self.selected_exercise_index is not None:
            if from_original_list and self.selected_exercise_index < len(self.original_workout_list.children):
                self.original_workout_list.children[self.selected_exercise_index].bg_color = (1, 1, 1, 1)
                self.original_workout_list.children[self.selected_exercise_index].text_color = (0, 0, 0, 1)
            elif not from_original_list and self.selected_exercise_index < len(self.additional_exercise_list.children):
                self.additional_exercise_list.children[self.selected_exercise_index].bg_color = (1, 1, 1, 1)
                self.additional_exercise_list.children[self.selected_exercise_index].text_color = (0, 0, 0, 1)

        # Select the new exercise
        if from_original_list:
            matching_children = list(filter(lambda x: x.text.split(':')[0].strip() == self.selected_exercise_name,
                                            self.original_workout_list.children))
            if matching_children:
                child = matching_children[0]
                child.bg_color = (0.2, 0.2, 0.2, 1)  # Set the background color for selected exercise
                child.text_color = (1, 1, 1, 1)  # Set the text color for selected exercise
                child.secondary_text = ""  # Clear the secondary text
                self.selected_exercise_index = self.original_workout_list.children.index(child)
        else:
            matching_children = list(
                filter(lambda x: x.text == self.selected_exercise_name, self.additional_exercise_list.children))
            if matching_children:
                child = matching_children[0]
                child.bg_color = (0.2, 0.2, 0.2, 1)  # Set the background color for selected exercise
                child.text_color = (1, 1, 1, 1)  # Set the text color for selected exercise
                self.selected_exercise_index = self.additional_exercise_list.children.index(child)

    def update_exercise(self, exercise_name, weight, reps, heart_rate):
        """
        Update the exercise with the given details and add it to the live workout list.

        Args:
            exercise_name (str): The name of the exercise.
            weight (int): The weight used in the exercise.
            reps (int): The number of repetitions performed.
            heart_rate (int): The heart rate during the exercise.
        """
        if weight > 0 and reps > 0 and heart_rate > 0:
            updated_details = f"{exercise_name}: {weight} lbs {reps} reps (HR: {heart_rate})"

            # Remove the exercise with zero weight and reps from the live_workout_list
            for child in self.live_workout_list.children[:]:
                if child.text.split(':')[0].strip() == exercise_name:
                    self.live_workout_list.remove_widget(child)
                    break

            live_workout_item = OneLineListItem(text=updated_details)
            self.live_workout_list.add_widget(live_workout_item)

            # Update the workout vector
            exercise_info = V.to_matrix_translation(exercise_name, weight, reps, heart_rate)
            self.new_workout_vector.append(exercise_info)

            # Store the exercise time and heart rate
            exercise_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.exercise_times.append((exercise_time, heart_rate))

            time_tracing.append(time.time())
            stress_tracing.append(weight * reps)
            print(f'time list : {time_tracing}\nstress : {stress_tracing}')

            # Calculate the metabolic efficiency
            muscle_group = self.get_muscle_group(exercise_name)
            metabolic_efficiency = self.calculate_metabolic_efficiency(muscle_group)
            print(f'{metabolic_efficiency}')

            # Get the exercise number from the filters class
            exercise_number = V.to_matrix_translation(exercise_name, 0, 0, 0)[0]

            # Store the exercise number and metabolic efficiency in the metabolic_evaluation list
            if metabolic_efficiency != 'Unavailable':
                try:
                    self.metabolic_evaluation.append([exercise_number, float(metabolic_efficiency)])
                except ValueError:
                    print(f"Invalid metabolic efficiency value: {metabolic_efficiency}")
            else:
                print(f"Metabolic efficiency unavailable for exercise: {exercise_name}")

            print(f'metabolic_evaluation : {self.metabolic_evaluation}')

            # Clear the weight, reps, and heart rate fields
            self.weight_field.text = ""
            self.reps_field.text = ""
            self.heart_rate_field.text = ""
        else:
            print(f"Invalid weight, reps, or heart rate for exercise: {exercise_name}")

    def end_workout(self, instance):
        """
        End the current workout and navigate to the workout summary screen.

        Args:
            instance: The instance of the button that triggered the event.
        """
        self.workout_end_time = time.time()  # Record the workout end time
        workout_duration = self.workout_end_time - self.workout_start_time  # Calculate the workout duration in seconds

        # Calculate the total weight x reps for the workout
        total_weight_reps = sum(exercise[1] * exercise[2] for exercise in self.new_workout_vector)

        # Calculate the stress dose (total weight x reps / workout duration)
        stress_dose = total_weight_reps / workout_duration

        # Get the current date
        current_date = datetime.date.today()

        # Create an instance of the WorkoutDesignScreen class
        workout_design_screen = WorkoutDesignScreen(client_selection_screen=self.client_selection_screen)
        workout_design_screen.client_id = self.client_id

        # Prepare the workout data
        workout_data = {
            'client_id': self.client_id,
            'workout_vector': self.new_workout_vector,
            'workout_date': current_date,
            'wo_type': workout_design_screen.det_workout(self.new_workout_vector),
            'workout_status': 'Complete',
            'time_total': workout_duration,
            'stress_dose': stress_dose
        }

        # Update the workout data in the database
        action = 'UPDATE'
        table = 'workouts'
        columns = ['workout_vector', 'wo_type', 'workout_status', 'time_total', 'stress_dose']
        values = [workout_data['workout_vector'], workout_data['wo_type'], workout_data['workout_status'],
                  workout_data['time_total'], workout_data['stress_dose']]
        where_columns = ['workouts_id']
        where_values = [self.workout_id]

        C.data_adjustment(action, table, columns, values, where_columns, where_values)

        C.data_adjustment(action, 'workouts', ['meta_efi'], [self.metabolic_evaluation], where_columns, where_values) # updates meta_efi in pgadmin4

        # Retrieve the updated workout vector from the database
        updated_workout_data = C.data_retrieval(table, ['workout_vector'], where_columns, where_values)
        updated_workout_vector = updated_workout_data[0][0] if updated_workout_data else []

        # Navigate to the WorkoutSummaryScreen and pass the live workout details and updated workout vector
        workout_summary_screen = self.manager.get_screen('workout_summary')
        workout_summary_screen.display_workout_summary(
            completed_exercises=[child.text for child in self.live_workout_list.children],
            updated_workout_vector=updated_workout_vector,
            exercise_times=self.exercise_times,  # Pass the exercise times to the workout summary screen
            stress_dose=stress_dose  # Pass the stress dose to the workout summary screen
        )
        self.manager.current = 'workout_summary'

    def on_pre_enter(self, *args):
        """
        Callback function called before entering the screen.
        """
        self.client_id = self.client_selection_screen.selected_client_id
        print(f"WorkoutDetailsScreen - Client ID: {self.client_id}")


class GoalsScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'goals'
        self.client_selection_screen = client_selection_screen

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create a layout for the "Back" button
        back_button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back
        )
        back_button_layout.add_widget(back_button)

        # Create a layout for entering goals and displaying previous goals
        content_layout = MDBoxLayout(orientation='vertical', spacing=20)

        # Create a layout for entering goals
        goal_entry_layout = MDBoxLayout(orientation='horizontal', spacing=10)
        self.goal_text_field = MDTextField(
            hint_text="Enter your goal",
            multiline=True,
            size_hint_x=0.7
        )
        add_goal_button = MDRectangleFlatButton(
            text="Add Goal",
            size_hint_x=0.3,
            on_release=self.add_goal
        )
        goal_entry_layout.add_widget(self.goal_text_field)
        goal_entry_layout.add_widget(add_goal_button)

        # Create a layout for displaying previous goals
        previous_goals_scroll = MDScrollView(size_hint_y=0.6)
        self.previous_goals_list = MDBoxLayout(orientation='vertical', spacing=10, padding=10)
        previous_goals_scroll.add_widget(self.previous_goals_list)

        content_layout.add_widget(goal_entry_layout)
        content_layout.add_widget(previous_goals_scroll)

        main_layout.add_widget(back_button_layout)
        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def on_pre_enter(self, *args):
        self.load_previous_goals()

    def go_back(self, instance):
        # Navigate back to the main screen
        self.manager.current = 'main'

    def add_goal(self, instance):
        goal_text = self.goal_text_field.text
        if goal_text.strip():
            # Insert the goal into the database
            client_id = self.client_selection_screen.selected_client_id
            goal_data = {
                'client_id': client_id,
                'a_goal': goal_text
            }
            action = 'INSERT'
            table = 'goals'
            columns = list(goal_data.keys())
            values = tuple(goal_data.values())

            C.data_adjustment(action, table, columns, values)

            # Clear the text field
            self.goal_text_field.text = ""

            # Reload the previous goals
            self.load_previous_goals()

    def load_previous_goals(self):
        # Retrieve previous goals from the database
        client_id = self.client_selection_screen.selected_client_id
        table = 'goals'
        columns = ['goals_id', 'client_id', 'a_goal']
        where_columns = ['client_id']
        where_values = [client_id]
        order_by = 'goals_id DESC'  # Order by goals_id in descending order

        previous_goals = C.data_retrieval(table, columns, where_columns=where_columns, where_values=where_values, order_by=order_by)

        # Clear the previous goals list
        self.previous_goals_list.clear_widgets()

        # Add the previous goals to the list
        for goal_id, _, goal_text in previous_goals:
            goal_layout = MDBoxLayout(orientation='horizontal', spacing=10)

            goal_label = MDLabel(
                text=goal_text,
                size_hint_x=0.7,
                size_hint_y=None,
                height=self.calculate_label_height(goal_text)
            )

            delete_button = MDRectangleFlatButton(
                text="Delete",
                size_hint_x=0.15,
                size_hint_y=None,
                height=40,
                on_release=lambda _, goal_id=goal_id: self.delete_goal(goal_id)
            )

            edit_button = MDRectangleFlatButton(
                text="Edit",
                size_hint_x=0.15,
                size_hint_y=None,
                height=40,
                on_release=lambda _, goal_id=goal_id, goal_text=goal_text: self.edit_goal(goal_id, goal_text)
            )

            goal_layout.add_widget(goal_label)
            goal_layout.add_widget(delete_button)
            goal_layout.add_widget(edit_button)

            self.previous_goals_list.add_widget(goal_layout)

    def calculate_label_height(self, text):
        label = MDLabel(text=text, font_style='Body1')
        return label.texture_size[1] + 10  # Add padding

    def delete_goal(self, goal_id):
        # Delete the goal from the database
        table = 'goals'
        where_columns = ['goals_id']
        where_values = [goal_id]

        C.data_adjustment('DELETE', table, [], [], where_columns, where_values)

        # Reload the previous goals
        self.load_previous_goals()

    def edit_goal(self, goal_id, goal_text):
        # Create a dialog box for editing the goal
        dialog = MDDialog(
            title="Edit Goal",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing=20,
                padding=20,
                size_hint_y=None,
                height=200,
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=lambda x: self.save_edited_goal(dialog, goal_id),
                ),
            ],
        )

        # Add a text field to the dialog box
        text_field = MDTextField(text=goal_text, multiline=True)
        dialog.content_cls.add_widget(text_field)

        # Open the dialog box
        dialog.open()

    def save_edited_goal(self, dialog, goal_id):
        # Get the new goal text from the text field
        new_goal_text = dialog.content_cls.children[0].text

        # Update the goal in the database
        table = 'goals'
        columns = ['a_goal']
        values = [new_goal_text]
        where_columns = ['goals_id']
        where_values = [goal_id]
        C.data_adjustment('UPDATE', table, columns, values, where_columns, where_values)

        # Dismiss the dialog box
        dialog.dismiss()

        # Reload the previous goals
        self.load_previous_goals()


class ProgressScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'progress'
        self.ids = {}
        self.client_selection_screen = client_selection_screen

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back,
            pos_hint={'center': 1, 'top': 1}
        )
        main_layout.add_widget(back_button)

        # Average lbs/sec and Workout Time
        stats_layout = MDBoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=50)
        self.avg_lbs_per_sec_label = MDLabel(text="Average lbs/sec: ", halign='left', valign='center', size_hint=(0.5, 1))
        self.avg_workout_time_label = MDLabel(text="Average Workout Time: ", halign='left', valign='center', size_hint=(0.5, 1))
        stats_layout.add_widget(self.avg_lbs_per_sec_label)
        stats_layout.add_widget(self.avg_workout_time_label)

        # Muscle Group List
        muscle_group_card = MDCard(orientation='vertical', padding=20, size_hint_y=None, height=300)
        muscle_group_title = MDLabel(text="Muscle Groups by Average Force", size_hint_y=None, height=50, bold=True)
        muscle_group_scroll = MDScrollView(size_hint_y=None, height=250)
        self.muscle_group_layout = MDBoxLayout(orientation='vertical', spacing=10, adaptive_height=True)
        self.ids['muscle_group_layout'] = self.muscle_group_layout
        self.muscle_group_labels = []
        muscle_group_scroll.add_widget(self.muscle_group_layout)
        muscle_group_card.add_widget(muscle_group_title)
        muscle_group_card.add_widget(muscle_group_scroll)

        # Workout DataFrame
        workout_df_card = MDCard(orientation='vertical', padding=20, size_hint_y=None, height=300)
        workout_df_title = MDLabel(text="Muscle-Metabolic Connection Statistics", size_hint_y=None, height=50, bold=True)
        workout_df_scroll = MDScrollView(size_hint_y=None, height=250)
        self.workout_df_layout = MDBoxLayout(orientation='vertical', spacing=10, adaptive_height=True)
        self.ids['workout_df_layout'] = self.workout_df_layout
        self.workout_df_labels = []
        workout_df_scroll.add_widget(self.workout_df_layout)
        workout_df_card.add_widget(workout_df_title)
        workout_df_card.add_widget(workout_df_scroll)

        main_layout.add_widget(stats_layout)
        main_layout.add_widget(muscle_group_card)
        main_layout.add_widget(workout_df_card)

        self.add_widget(main_layout)

    def go_back(self, instance):
        # Navigate back to the main screen
        self.manager.current = 'main'

    def on_pre_enter(self, *args):
        try:
            self.fetch_and_display_progress()
        except Exception as e:
            print(f"Error occurred: {e}")

            self.show_no_workout_popup()

    def show_no_workout_popup(self):
        dialog = MDDialog(
            title="No Workout Data",
            text="A workout needs to be completed first before viewing progress.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dismiss_dialog_and_go_back(dialog)
                )
            ]
        )
        dialog.open()

    def dismiss_dialog_and_go_back(self, dialog):
        dialog.dismiss()
        self.manager.current = 'main'

    def fetch_and_display_progress(self):
        # Fetch data from the database
        client_id = self.client_selection_screen.selected_client_id
        print(f'CURRENT CLIENT ID: {client_id}')

        # Call the display_workout_data function from Calculations.py
        df = display_workout_data(client_id)

        if df.empty:
            raise ValueError("No workout data available")

        # Display the DataFrame with metabolic efficiency scores
        self.display_workout_df(df)

        table = 'workouts'
        columns = ['stress_dose', 'time_total', 'wo_type']
        where_columns = ['client_id']
        where_values = [client_id]

        workout_data = C.data_retrieval(table, columns, where_columns=where_columns, where_values=where_values)

        if not workout_data:
            raise ValueError("No workout data available")

        # Calculate averages
        total_stress_dose = 0
        total_workout_time = 0
        num_workouts = 0
        muscle_group_force = defaultdict(list)
        muscle_group_times = defaultdict(list)  # Dictionary to store workout times for each muscle group

        for stress_dose, workout_time, wo_type in workout_data:
            if stress_dose is not None and workout_time is not None:
                total_stress_dose += stress_dose
                total_workout_time += workout_time
                muscle_groups = self.extract_muscle_group(wo_type)
                for muscle_group in muscle_groups:
                    muscle_group_force[muscle_group].append(stress_dose * workout_time)
                    muscle_group_times[muscle_group].append(workout_time)  # Store the workout time for each muscle group
                num_workouts += 1

        if num_workouts > 0:
            avg_lbs_per_sec = total_stress_dose / num_workouts
            avg_workout_time = total_workout_time / num_workouts
        else:
            avg_lbs_per_sec = 0
            avg_workout_time = 0

        # Display averages
        self.avg_lbs_per_sec_label.text = f"Average lbs/sec: {avg_lbs_per_sec:.2f}"
        self.avg_workout_time_label.text = f"Average Workout Time: {avg_workout_time:.2f} seconds"

        # Calculate average force and average time for each muscle group
        muscle_group_avg_force = {}
        muscle_group_avg_time = {}
        for group, forces in muscle_group_force.items():
            muscle_group_avg_force[group] = sum(forces) / len(forces) if forces else 0
        for group, times in muscle_group_times.items():
            muscle_group_avg_time[group] = sum(times) / len(times) if times else 0

        # Sort muscle groups by average force in descending order
        sorted_muscle_groups = sorted(muscle_group_avg_force.items(), key=lambda x: x[1], reverse=True)

        # Display muscle group list
        self.display_muscle_group_list(sorted_muscle_groups, muscle_group_avg_time)

    def display_workout_df(self, df):
        # Clear previous DataFrame labels
        for label in self.workout_df_labels:
            self.ids.workout_df_layout.remove_widget(label)
        self.workout_df_labels.clear()

        # Calculate the total average
        total_average = df['Average'].sum()

        # Sort the DataFrame by the 'Average' column in descending order
        df = df.sort_values(by='Average', ascending=False)

        # Retrieve the client's body weight from the database
        client_id = self.client_selection_screen.selected_client_id
        table = 'clients'
        columns = ['weight']
        where_columns = ['client_id']
        where_values = [client_id]

        client_data = C.data_retrieval(table, columns, where_columns, where_values)

        if client_data and client_data[0][0] is not None:
            body_weight = float(client_data[0][0])
        else:
            print("Client body weight not found. Using default value.")
            body_weight = 1

        # Calculate the average metabolic efficiency score for each exercise
        metabolic_efficiency_scores = {}
        for index, row in df.iterrows():
            exercise_id = list(exercise_matrix.keys())[list(exercise_matrix.values()).index(row['x'])]
            metabolic_efficiency = self.calculate_average_metabolic_efficiency(exercise_id)
            metabolic_efficiency_scores[row['x']] = metabolic_efficiency

        # Add new DataFrame labels with percentages, systemic response, and metabolic efficiency
        for index, row in df.iterrows():
            percentage = (row['Average'] / total_average) * 100 if total_average != 0 else 0
            systemic_response = row['Average'] / body_weight
            metabolic_efficiency = metabolic_efficiency_scores[row['x']]
            label_text = f"{row['x']}: {row['Average']:.2f} MR -- {percentage:.2f}% T -- {systemic_response:.2f} SR -- {metabolic_efficiency:.2f} ME"
            label = MDLabel(text=label_text, halign='left', valign='center', size_hint=(1, None), height=30)
            self.ids.workout_df_layout.add_widget(label)
            self.workout_df_labels.append(label)

    def calculate_average_metabolic_efficiency(self, exercise_id):
        client_id = self.client_selection_screen.selected_client_id

        # Retrieve the necessary measurements from the database
        table = 'clients'
        columns = ['vt1', 'heart_rate_descent']
        where_columns = ['client_id']
        where_values = [client_id]

        measurements = C.data_retrieval(table, columns, where_columns, where_values)

        if measurements:
            vt1, heart_rate_descent = measurements[0]

            # Check if all measurements are available
            if all(value is not None for value in measurements[0]):
                # Retrieve the workout data for the specific exercise
                table = 'workouts'
                columns = ['workout_vector', 'time_total']
                where_columns = ['client_id']
                where_values = [client_id]

                workout_data = C.data_retrieval(table, columns, where_columns, where_values)

                total_metabolic_efficiency = 0
                count = 0

                for workout in workout_data:
                    workout_vector = workout[0]
                    time_total = workout[1]

                    for exercise_info in workout_vector:
                        if exercise_info[0] == exercise_id:
                            weight = exercise_info[1]
                            reps = exercise_info[2]
                            heart_rate = exercise_info[3]

                            # Calculate the metabolic efficiency for the exercise
                            metabolic_efficiency = self.calculate_metabolic_efficiency(weight, reps, heart_rate, vt1, heart_rate_descent, time_total)
                            total_metabolic_efficiency += metabolic_efficiency
                            count += 1

                if count > 0:
                    return total_metabolic_efficiency / count
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    def calculate_metabolic_efficiency(self, weight, reps, heart_rate, vt1, heart_rate_descent, time_total):
        try:
            # Retrieve the client's body weight from the database
            client_id = self.client_selection_screen.selected_client_id
            table = 'clients'
            columns = ['weight']
            where_columns = ['client_id']
            where_values = [client_id]

            client_data = C.data_retrieval(table, columns, where_columns, where_values)

            if client_data and client_data[0][0] is not None:
                body_weight = float(client_data[0][0])
            else:
                print("Client body weight not found. Using default value.")
                body_weight = 1  # Default value if not found

            print(f"weight: {weight}, type: {type(weight)}")
            print(f"reps: {reps}, type: {type(reps)}")
            print(f"time_total: {time_total}, type: {type(time_total)}")
            print(f"vt1: {vt1}, type: {type(vt1)}")
            print(f"heart_rate_descent: {heart_rate_descent}, type: {type(heart_rate_descent)}")
            print(f"body_weight: {body_weight}, type: {type(body_weight)}")

            weight = float(weight)
            reps = float(reps)
            time_total = float(time_total)
            vt1 = float(vt1)
            heart_rate = float(heart_rate)
            heart_rate_descent = float(heart_rate_descent)

            weight_reps_per_min = weight * reps / (time_total / 60)
            vt1_max_hr_ratio = vt1 / heart_rate
            max_hr_descent_ratio = heart_rate / heart_rate_descent

            # Incorporate body weight into the metabolic efficiency calculation
            metabolic_efficiency = (weight_reps_per_min * vt1_max_hr_ratio * max_hr_descent_ratio) / body_weight
            return metabolic_efficiency

        except (TypeError, ValueError) as e:
            print(f"Error in calculate_metabolic_efficiency: {str(e)}")
            return 0

        except ZeroDivisionError as e:
            print(f"Error in calculate_metabolic_efficiency: {str(e)}")
            return 0

    def display_muscle_group_list(self, sorted_muscle_groups, muscle_group_avg_time):
        # Clear previous muscle group labels
        for label in self.muscle_group_labels:
            self.ids.muscle_group_layout.remove_widget(label)
        self.muscle_group_labels.clear()

        # Add new muscle group labels with average force and average time
        for muscle_group, avg_force in sorted_muscle_groups:
            avg_time = muscle_group_avg_time[muscle_group]
            label_text = f"{muscle_group}: {avg_force:.2f} lbs, {avg_time:.2f} seconds"
            label = MDLabel(text=label_text, halign='left', valign='center', size_hint=(1, None), height=30)
            self.ids.muscle_group_layout.add_widget(label)
            self.muscle_group_labels.append(label)

    def extract_muscle_group(self, wo_type):
        # List of possible muscle group names
        muscle_groups = ['Pull', 'Push', 'Shoulders', 'Legs', 'Arms']

        # Create a list to store the matching muscle groups
        matching_groups = []

        # Check if the wo_type string contains any of the muscle group names
        for group in muscle_groups:
            if group.lower() in wo_type.lower():
                matching_groups.append(group)

        # If no muscle group is found, return ['Unknown']
        return matching_groups if matching_groups else ['Unknown']





class TestingScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'testing'
        self.client_selection_screen = client_selection_screen

        # Main layout
        main_layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        # Scroll view for test fields
        scroll_view = ScrollView(size_hint=(1, 1))
        self.fields_layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        self.fields_layout.bind(minimum_height=self.fields_layout.setter('height'))

        self.test_fields = {
            'weight': {'hint': "Enter Body Weight", 'column': 'weight'},
            'vt1': {'hint': "Enter VT1 value", 'column': 'vt1'},
            'heart_rate_descent': {'hint': "Enter Heart Rate Descent value", 'column': 'heart_rate_descent'},
            'squat_1rm': {'hint': "Enter Squat 1RM", 'column': 'squat_1rm'},
            'dead_lift_1rm': {'hint': "Enter Dead Lift 1RM", 'column': 'dead_lift_1rm'},
            'bench_1rm': {'hint': "Enter Bench 1RM", 'column': 'bench_1rm'},
            'lat_pull_1rm': {'hint': "Enter Lat Pull 1RM", 'column': 'lat_pull_1rm'},
            'shoulder_press_1rm': {'hint': "Enter Shoulder Press 1RM", 'column': 'shoulder_press_1rm'},
            'row_1rm': {'hint': "Enter Row 1RM", 'column': 'row_1rm'},
            'vo2_max': {'hint': "Enter Vo2 Max", 'column': 'vo2_max'}
        }

        for key, value in self.test_fields.items():
            value['input'] = MDTextField(
                hint_text=value['hint'],
                size_hint_y=None,
                height=50
            )
            self.fields_layout.add_widget(value['input'])

        scroll_view.add_widget(self.fields_layout)
        main_layout.add_widget(scroll_view)

        # Update button
        update_button = MDRectangleFlatButton(
            text="Update All Changes",
            on_release=self.update_all_changes,
            size_hint=(1, None),
            height=50
        )
        main_layout.add_widget(update_button)

        # Back button (now under the update button)
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back,
            size_hint=(1, None),
            height=50
        )
        main_layout.add_widget(back_button)

        # Status label
        self.status_label = MDLabel(
            text="",
            halign='center',
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(self.status_label)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.current = 'main'

    def update_all_changes(self, instance):
        client_id = self.client_selection_screen.selected_client_id
        table = 'clients'
        columns = []
        values = []
        updated_fields = []

        for key, value in self.test_fields.items():
            input_text = value['input'].text.strip()
            if input_text:
                try:
                    float_value = float(input_text)
                    columns.append(value['column'])
                    values.append(float_value)
                    updated_fields.append(key)
                except ValueError:
                    self.status_label.text = f"Invalid value for {key.replace('_', ' ').title()}"
                    return

        if columns and values:
            where_columns = ['client_id']
            where_values = [client_id]

            C.data_adjustment('UPDATE', table, columns, values, where_columns, where_values)
            print(f"Attempting to update {', '.join(updated_fields)} for client {client_id}")

            # Clear the input fields that were successfully updated
            for key in updated_fields:
                self.test_fields[key]['input'].text = ""
        else:
            self.status_label.text = "No changes to update"


class BioMetricsScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'biometrics'
        self.client_selection_screen = client_selection_screen

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create a layout for the "Back" button
        back_button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back
        )
        back_button_layout.add_widget(back_button)

        # Create text field for weight
        self.weight_field = MDTextField(
            hint_text="Body Weight (lbs)",
            size_hint=(1, None),
            height=50
        )
        main_layout.add_widget(self.weight_field)

        # Create text fields for measurements
        self.measurement_fields = {}
        measurements = ['Neck', 'Chest', 'Left Arm', 'Left Forearm', 'Right Arm', 'Right Forearm', 'Waist', 'Hips',
                        'Left Thigh', 'Right Thigh', 'Left Calf', 'Right Calf']
        for measurement in measurements:
            text_field = MDTextField(
                hint_text=measurement,
                size_hint=(1, None),
                height=50
            )
            self.measurement_fields[measurement.lower().replace(' ', '_') + '_mes'] = text_field
            main_layout.add_widget(text_field)

        # Create a "Save" button
        save_button = MDRectangleFlatButton(
            text="Save",
            size_hint=(1, None),
            height=50,
            on_release=self.save_measurements
        )
        main_layout.add_widget(save_button)

        main_layout.add_widget(back_button_layout)

        self.add_widget(main_layout)

    def on_pre_enter(self, *args):
        # Load existing measurements when entering the screen
        self.load_existing_measurements()

    def go_back(self, instance):
        self.manager.current = 'documents_notes'

    def load_existing_measurements(self):
        client_id = self.client_selection_screen.selected_client_id
        table = 'clients'
        columns = ['weight'] + list(self.measurement_fields.keys())
        where_columns = ['client_id']
        where_values = [client_id]

        existing_data = C.data_retrieval(table, columns, where_columns, where_values)

        if existing_data:
            # Populate weight field
            self.weight_field.text = str(existing_data[0][0] or '')

            # Populate other measurement fields
            for i, field in enumerate(self.measurement_fields.keys(), start=1):
                self.measurement_fields[field].text = str(existing_data[0][i] or '')

    def save_measurements(self, instance):
        client_id = self.client_selection_screen.selected_client_id
        measurement_data = {}

        # Add weight to measurement_data
        weight = self.weight_field.text.strip()
        if weight:
            try:
                measurement_data['weight'] = float(weight)
            except ValueError:
                # Handle invalid input values
                measurement_data['weight'] = None
        else:
            # Handle empty input values
            measurement_data['weight'] = None

        for field in self.measurement_fields:
            value = self.measurement_fields[field].text.strip()
            if value:
                try:
                    measurement_data[field] = float(value)
                except ValueError:
                    # Handle invalid input values
                    measurement_data[field] = None
            else:
                # Handle empty input values
                measurement_data[field] = None

        # Update the measurements in the 'clients' table
        table = 'clients'
        columns = list(measurement_data.keys())
        values = tuple(measurement_data.values())
        where_columns = ['client_id']
        where_values = [client_id]

        C.data_adjustment('UPDATE', table, columns, values, where_columns, where_values)

        # Show a confirmation message
        self.show_confirmation_dialog()

    def show_confirmation_dialog(self):
        dialog = MDDialog(
            title="Measurements Saved",
            text="The measurements have been successfully updated.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dismiss_dialog_and_go_back(dialog)
                )
            ]
        )
        dialog.open()

    def dismiss_dialog_and_go_back(self, dialog):
        dialog.dismiss()
        self.manager.current = 'documents_notes'


class DocumentsNotesScreen(MDScreen):
    def __init__(self, client_selection_screen, **kwargs):
        super().__init__(**kwargs)
        self.name = 'documents_notes'
        self.client_selection_screen = client_selection_screen

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        # Create a layout for the "Back" button
        back_button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.go_back
        )
        back_button_layout.add_widget(back_button)

        # Create a text field
        self.text_input = MDTextFieldRect(
            hint_text="Enter text here",
            multiline=True,
            size_hint_y=0.5
        )

        # Create a layout for the buttons
        buttons_layout = MDBoxLayout(orientation='vertical', spacing=10)
        buttons = ['PARQ', 'Heart Disease Risk', 'Legal Documents', 'Transactions', 'Client Notes', 'Measurement']  # Add 'Measurement' button
        for button_text in buttons:
            button = MDRectangleFlatButton(
                text=button_text,
                size_hint=(1, None),
                height=50,
                on_release=self.button_callback
            )
            buttons_layout.add_widget(button)

        main_layout.add_widget(back_button_layout)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(buttons_layout)

        self.add_widget(main_layout)

    def button_callback(self, instance):
        if instance.text == 'Measurement':
            self.manager.current = 'biometrics'
        else:
            self.save_data(instance)

    def go_back(self, instance):
        # Navigate back to the main screen
        self.manager.current = 'main'

    def save_data(self, instance):
        document_type = instance.text
        text_input = self.text_input.text

        if not text_input:
            # If the text field is empty, don't do anything
            return

        client_id = self.client_selection_screen.selected_client_id  # Use the selected client ID

        if document_type == 'PARQ':
            column = 'parq_score'
            value = text_input
        elif document_type == 'Heart Disease Risk':
            column = 'heart_disease_risk'
            value = text_input
        elif document_type == 'Legal Documents':
            column = '"Legal Documents"'
            value = text_input
        elif document_type == 'Transactions':
            column = '"Transactions"'
            value = text_input
        elif document_type == 'Client Notes':
            column = '"Client Notes"'
            value = text_input
        else:
            print(f"Invalid document type: {document_type}")
            return

        # Update the corresponding column in the "clients" table
        C.data_adjustment(
            action='UPDATE',
            table='clients',
            columns=[column],
            values=[value],
            where_columns=['client_id'],
            where_values=[client_id]
        )


class WorkoutSummaryScreen(MDScreen):
    def __init__(self, client_id, **kwargs):
        super().__init__(**kwargs)
        self.name = 'workout_summary'
        self.client_id = client_id

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20)

        self.back_button = MDRectangleFlatButton(text='Return Home', on_release=self.ret_home)

        # Create a scroll view for the completed exercises
        completed_exercises_scroll = MDScrollView(size_hint=(1, 0.4))
        self.completed_exercises_list = MDList()
        completed_exercises_scroll.add_widget(self.completed_exercises_list)


        # Create a label for displaying the stress dose
        self.stress_dose_label = MDLabel(
            text="Stress Dose: ",
            halign='left',
            valign='top',
            size_hint=(1, None),
            height=40
        )

        main_layout.add_widget(completed_exercises_scroll)
        main_layout.add_widget(self.stress_dose_label)
        main_layout.add_widget(self.back_button)

        self.add_widget(main_layout)


    def ret_home(self, instance):
        self.manager.current = 'main'

    def display_workout_summary(self, completed_exercises, updated_workout_vector, exercise_times, stress_dose):
        # Clear the previous completed exercises list
        self.completed_exercises_list.clear_widgets()

        # Add the completed exercises to the list
        for exercise in completed_exercises:
            completed_exercise_item = OneLineListItem(text=exercise)
            self.completed_exercises_list.add_widget(completed_exercise_item)

        # Display the updated workout vector
        workout_vector_text = str(updated_workout_vector).replace('], [', '],\n[')

        # Display the stress dose
        self.stress_dose_label.text = f"Stress Dose: {stress_dose:.2f} lbs/sec"

        self.completed_exercises = completed_exercises


if __name__ == '__main__':
    WorkoutPlannerApp().run()