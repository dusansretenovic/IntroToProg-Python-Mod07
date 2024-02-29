# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#  DusanS,2/22/2024,Created Script
#  DusanS, 2/29/2024, Amended Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

#  Create a Person Class
class Person:
    """
    This class contains the person's first name and last name
        DusanS,2/22/2024,Created class Person

    """

    # Add first_name and last_name properties to the constructor

    def __init__(self, first_name:str = "", last_name:str = ""):
        self.__first_name = first_name
        self.__last_name = last_name

    # Create a getter and setter for the first_name property
    @property
    def first_name(self):
        return self.__first_name.capitalize()

    @first_name.setter
    def first_name(self, value:str):
        if value.isalpha():
            self.__first_name = value
        else:
            raise ValueError(f"First name can only contain alphabetical characters.")

    # Create a getter and setter for the last_name property
    @property
    def last_name(self):
        return self.__last_name.capitalize()

    @last_name.setter
    def last_name(self, value:str):
        if value.isalpha():
            self.__last_name = value
        else:
            raise ValueError(f"Last name can only contain alphabetical characters.")

    # Override the __str__() method to return Person data
    def __str__(self):
        return f"{self.first_name},{self.last_name}"

# Create a Student class the inherits from the Person class
class Student(Person):
    """
        This class inherits the Person class properties and adds the course_name property
            DusanS,2/22/2024,Created class Person

    """
    # Call to the Person constructor and pass it the first_name and last_name data
    def __init__(self, first_name:str = "", last_name:str = "", course_name:str = ""):
        super().__init__(first_name=first_name, last_name=last_name)

        # Add an assignment to the course_name property using the course_name parameter
        self.course_name = course_name

        # Add the getter for course_name
        @property
        def course_name(self):
            return self.__course_name

        # Add the setter for course_name
        @course_name.setter
        def course_name(self, value: str):
            self.__course_name = value

    #Override the __str__() method to return the Student data
    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.course_name}"

class FileProcessor:
    """
    This class contains functions designed to work with JSON files, reading data and writing it to file.
        DusanS,2/19/2024,Created class File Processor
        DusanS, 2/29/2024, Amended Script
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[Student]):
        """
        This function reads the json file and stores the data into a list of Student object rows.
            DusanS,2/19/2024,Created function read_data_from_file

        """
        file_data = []
        file = None

        try:
            file = open(file_name, "r")
            file_data = json.load(file)
            for student in file_data:
                student_object: Student = Student(first_name=student["FirstName"], last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)
                file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[Student]):
        """
        This function writes the data from a list of Student objects to a json file.
            DusanS,2/19/2024,Created function write_data_to_file
            DusanS, 2/29/2024, Amended Script
        """
        try:
            file = open(file_name, "w")
            file_data = []
            for student in student_data:
                file_data.append({"FirstName": student.first_name, "LastName": student.last_name,
                                         "CourseName": student.course_name})
            json.dump(file_data, file)
            file.close()
            print("The following data was saved to file!\n")
            IO.output_student_course(student_data=student_data)
        except Exception as e:
            if not file.closed:
                file.close()
            IO.output_error_messages("There was a problem saving data to file.", e)

class IO:
    """
    This class contains functions designed to manage user input and output.
        DusanS,2/19/2024,Created class IO
        DusanS, 2/29/2024, Amended Script
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays a custom error message to the user.
            DusanS,2/19/2024,Created function output_error_messages
        """
        print(message, end="\n")
        if error is not None:
            print("-- Technical Error Message --")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays a menu of choices to the user.
            DusanS,2/19/2024,Created function output_menu

        """
        print(menu, end="\n")

    @staticmethod
    def input_menu_choice():
        """
        This function gets the user input from the menu of choices.
            DusanS,2/19/2024,Created function input_menu_choice
            DusanS, 2/29/2024, Amended Script
        """
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__()) #not passing e to avoid a technical message
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """
        This function gets the user input for the student's first name, last name and course name.
            DusanS,2/19/2024,Created function input_student_data
            DusanS, 2/29/2024, Amended Script
        """
        try:
            student = Student()
            student.first_name = input("Enter the student's first name: ")
            if not student.first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            student.last_name = input("Enter the student's last name: ")
            if not student.last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            student.course_name = input("Please enter the name of the course: ")
            student_data.append(student)
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages("User input can only contain alphabetical characters.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return students

    @staticmethod
    def output_student_course(student_data: list):
        """
        This function displays the course information to the user.
            DusanS,2/19/2024,Created function output_student_course
            DusanS, 2/29/2024, Amended Script
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

# End of function definitions

# Main body of this script


students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_course(student_data=students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break  # out of the loop

    else:
        print("Invalid option, please only choose one of the following: 1,2,3 or 4.")

print("Program ended.")


