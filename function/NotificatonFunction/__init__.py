import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info(
        'Python ServiceBus queue trigger processed message: %s',
        notification_id
    )

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=5432,
            sslmode="require"
        )
        cursor = conn.cursor()

       # ----------------------------
        # Get notification subject & message
        # ----------------------------
        cursor.execute("""
            SELECT subject, message
            FROM notification
            WHERE id = %s
        """, (notification_id,))
        result = cursor.fetchone()
        if not result:
            logging.warning(f"No notification found with ID {notification_id}")
            return
        
        subject, message = result
        # ----------------------------
        #  Get attendees
        # ----------------------------
        # Note: attendee table doesn't have notification_id, adjust if needed
        cursor.execute("""
            SELECT email, first_name
            FROM attendee
        """)
        attendees = cursor.fetchall()

        if not attendees:
            logging.info("No attendees found to notify.")
            return

        # ----------------------------
        # Send emails
        # ----------------------------
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        from_email = os.getenv("FROM_EMAIL")

        notified_count = 0
        for email, first_name in attendees:
            personalized_subject = f"{subject} - Hello {first_name} - This is email to inform about new notification"
            mail = Mail(
                from_email=from_email,
                to_emails=email,
                subject=personalized_subject,
                html_content=f"""
                <html>
                <body>
                    <h3>{subject}</h3>
                    <p>Hello {first_name},</p>
                    <p>{message or 'You have a new notification.'}</p>
                    <br/>
                    <p>Regards,<br/>TechConf Team</p>
                </body>
                </html>
                """
            )
            response = sg.send(mail)
            logging.info(
                f"Email sent to {email}, status {response.status_code}, "
                f"message-id {response.headers.get('X-Message-Id')}"
            )

            notified_count += 1

        # ----------------------------
        # Update notification status
        # ----------------------------
        cursor.execute("""
            UPDATE notification
            SET completed_date = %s,
                status = %s
            WHERE id = %s
        """, (
            datetime.utcnow(),
            f"Completed - {notified_count} notified",
            notification_id
        ))
        conn.commit()
        logging.info(f"Notification {notification_id} processed successfully.")
        
    except Exception as error:
        logging.error("Error processing notification", exc_info=True)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()