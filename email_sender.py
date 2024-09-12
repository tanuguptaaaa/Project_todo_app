import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import mysql.connector  # Ensure you're importing the correct MySQL connector

# Set up the email server
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Login credentials for sending the email (use environment variables for better security)
sender_email = 'guptatanu842002@gmail.com'
sender_password = 'wsoj jraw dnqx xioo'  # Store this in a secure manner

def send_email(Task_id,Email_id, Due_date,Title):


    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = Email_id
    msg['Subject'] = f'Update on Task: {Title}'

    # Email body
    body = f"Hello, here are the details for Task {Task_id}:\nTitle:{Title}\nDue_date:{Due_date}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Start the server and login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, Email_id, msg.as_string())
        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    finally:
        # Close the email server connection
        server.quit()

# Usage Example
# You would call send_email with a valid email, task ID, and database connection
# conn = mysql.connector.connect(user='user', password='password', host='localhost', database='your_db')
# send_email('recipient@example.com', 123, conn)

