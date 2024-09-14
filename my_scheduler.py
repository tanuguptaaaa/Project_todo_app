from apscheduler.schedulers.blocking import BlockingScheduler

from email_sender import send_email

from to_dolist import ToDo

def fetch_email():
    try:
        todo = ToDo()  # Assuming ToDo class connects to the database
        print("inside fetch_email")

        query = '''
        SELECT task.Task_id, users.Email_id,task.Title,task.Due_date
        FROM users
        INNER JOIN task ON users.id = task.User_id
        WHERE task.status = 'Pending'
        '''
        todo.cursor.execute(query)
        tasks = todo.cursor.fetchall()

        if tasks:
            print("\nPending Tasks (Email):")
            for task in tasks:
                Task_id = task[0]
                Email_id = task[1]
                Due_date = task[2]
                Title=task[3]

                # Send email


                email_sent = send_email(Task_id,Email_id, Due_date,Title)

                if email_sent:
                    # Update the task status to 'Complete' after sending the email
                    update_query = '''
                                UPDATE task
                                SET status = 'Complete'
                                WHERE Task_id = %s
                                '''
                    todo.cursor.execute(update_query, (Task_id ,))
                    todo.connection.commit()
                    print(f"Task {Task_id } marked as complete.")
                else:
                    print(f"Failed to send email to {Email_id} for task {Task_id}.")
        else:
            print("No pending tasks.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close cursor and connection
        if todo.cursor:
            todo.cursor.close()
        if todo.connection:
            todo.connection.close()




# Create a scheduler
scheduler = BlockingScheduler()
scheduler.add_job(fetch_email, 'interval', seconds=10)

# Start the scheduler
scheduler.start()
