from datetime import datetime

import mysql.connector
from mysql.connector import Error


class ToDo:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.logged_in_user_id = None

        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Anny@626',
                database='todolistdb'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error: {e}")

    def signup(self, first_name, last_name, email_id, password):
        try:
            query = '''INSERT INTO Users (First_name, Last_name, Email_id, Password, created_at)
                       VALUES (%s, %s, %s, %s, %s)'''
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute(query, (first_name, last_name, email_id, password, created_at))
            self.connection.commit()
            print("Signup successful")
        except Error as e:
            print(f"Error: {e}")

    def login(self, email_id, password):
        try:
            query = '''SELECT * FROM Users WHERE Email_id = %s'''
            self.cursor.execute(query, (email_id,))
            result = self.cursor.fetchone()
            if result and result[4] == password:
                print("Login successful!")
                self.logged_in_user_id = result[0]
                return True
            else:
                print("Invalid email or password.")
                return False
        except Error as e:
            print(f"Error: {e}")
            return False

    def add_task(self, title, description, status, due_date, task_type):
        try:
            query = '''INSERT INTO Task (User_id, Title, Description, Status, Due_date, Task_type)
                       VALUES (%s, %s, %s, %s, %s, %s)'''
            params = (self.logged_in_user_id, title, description, status, due_date, task_type)
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Task added successfully")
        except Error as e:
            print(f"Error: {e}")

    def update_task(self, task_id, title, description, status, due_date, task_type):
        try:
            query = '''UPDATE Task
                       SET Title = %s, Description = %s, Status = %s, Due_date = %s, Task_type = %s
                       WHERE Task_id = %s'''
            params = (title, description, status, due_date, task_type, task_id)
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Task updated successfully")
        except Error as e:
            print(f"Error: {e}")

    def delete_task(self, task_id):
        try:
            query = '''DELETE FROM Task WHERE Task_id = %s'''
            self.cursor.execute(query, (task_id,))
            self.connection.commit()
            print("Task deleted successfully")
        except Error as e:
            print(f"Error: {e}")

    def list_task(self):
        try:
            query='''Select Task_id,title,description,status,due_date,task_type
            from task where User_id=%s'''
            self.cursor.execute(query,(self.logged_in_user_id,))
            tasks=self.cursor.fetchall()
            if tasks:
                print("\nYour Tasks:")
                for task in tasks:
                    print(
                        f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}, Due Date: {task[4]}, Type: {task[5]}")
            else:
                print("No tasks found.")
        except Error as e:
            print(f"Error: {e}")


    def main_menu(self):
        while True:
            print("\nTO-DO List Menu")
            print("1. Login")
            print("2. Signup")
            print("3. Quit")

            choice = input("Select an option (1-3): ")

            if choice == '1':
                email_id = input("Enter Email ID: ")
                password = input("Enter Password: ")
                if self.login(email_id, password):
                    self.after_login()
            elif choice == '2':
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                email_id = input("Enter Your Email ID: ")
                password = input("Enter Password: ")
                self.signup(first_name, last_name, email_id, password)
            elif choice == '3':
                print("Thank you for using the TO-DO List.")
                break
            else:
                print("Invalid option. Please select a valid option.")

    def after_login(self):
        while True:
            print("\nAFTER Login Menu")
            print("1. Add to the list")
            print("2. Update the list")
            print("3. Delete from the list")
            print("4. list of the task")
            print("5. Exit")
            choice = input("Select an option (1-4): ")

            if choice == '1':
                title = input("Enter Task Title: ")
                description = input("Enter Task Description: ")
                status = input("Enter new Task Status (pending/done): ")
                due_date = input("Enter Task Due Date (YYYY-MM-DD): ")
                task_type = input("Enter Task Type: ")
                self.add_task(title, description,status, due_date, task_type)
                # self.task()
            elif choice == '2':
                task_id = input("Enter Task ID to update: ")
                title = input("Enter new Task Title: ")
                description = input("Enter new Task Description: ")
                status = input("Enter new Task Status (pending/done): ")
                due_date = input("Enter new Task Due Date (YYYY-MM-DD): ")
                task_type = input("Enter new Task Type: ")
                self.update_task(task_id, title, description,status,due_date, task_type)
            elif choice == '3':
                task_id = input("Enter Task ID to delete: ")
                self.delete_task(task_id)
            elif choice == '4':
                self.list_task()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please select a valid option.")


if __name__ == "__main__":
    todolist = ToDo()
    todolist.main_menu()
