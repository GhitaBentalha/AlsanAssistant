import sys
import os
import re
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from groq import Groq  # Assurez-vous d'avoir la bibliothèque Groq installée

# Un dictionnaire pour stocker les comptes (en mémoire)
accounts = {
    "israe": "123" 
}

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login & Sign Up - Chatbot d'Alsan Maroc")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")  # Light gray background

        # Create a stacked widget to switch between Login and Sign Up
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of both the LoginUI and SignUpUI
        self.login_ui = LoginUI(self)
        self.signup_ui = SignUpUI(self)

        # Add both UIs to the stacked widget
        self.stacked_widget.addWidget(self.login_ui)
        self.stacked_widget.addWidget(self.signup_ui)

        # Show the LoginUI by default
        self.stacked_widget.setCurrentWidget(self.login_ui)

    def switch_to_signup(self):
        self.stacked_widget.setCurrentWidget(self.signup_ui)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_ui)


class LoginUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                padding: 20px;
            }
            QWidget#form_container {
                background: #000000;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #444444;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #c41b1c;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #ca3233;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 20, 50, 70)

        self.logo_label = QLabel()
        pixmap = QPixmap('images/logo.png')  # Replace with your logo path
        if not pixmap.isNull():
            pixmap = pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignRight)
        self.logo_label.setStyleSheet("background: transparent;")
        self.layout.addWidget(self.logo_label)

        self.form_container = QWidget()
        self.form_container.setObjectName("form_container")
        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.setContentsMargins(30, 20, 30, 20)

        self.logo_label = QLabel()
        pixmap = QPixmap('images/log.png')  # Replace with your logo path
        if not pixmap.isNull():
            pixmap = pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")
        self.form_layout.addWidget(self.logo_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Id d'utilisateur")
        self.form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        self.form_layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Créer un compte")
        self.signup_button.clicked.connect(self.open_signup_ui)
        self.form_layout.addWidget(self.signup_button)

        self.layout.addWidget(self.form_container)

        self.social_media_layout = QHBoxLayout()
        self.social_media_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.social_media_layout)

        self.add_social_icon("images/insta.png", "https://www.instagram.com/alsan_world/")
        self.add_social_icon("images/linkedin.png", "https://www.linkedin.com/company/alsan/")
        self.add_social_icon("images/youtube.png", "https://www.youtube.com/user/AlvarezSchaer")
        self.add_social_icon("images/facebook.png", "https://web.facebook.com/alsanalvarezschaer/?_rdc=1&_rdr")

    def add_social_icon(self, image_path, link):
        icon_button = QPushButton()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Social media icon not found: {image_path}")  # Debug message
            return
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        icon_button.setIcon(QIcon(pixmap))
        icon_button.setIconSize(pixmap.size())
        icon_button.setFlat(True)
        icon_button.setStyleSheet("background-color: #ffffff; border-radius: 5px; padding: 5px;")
        icon_button.clicked.connect(lambda: self.open_link(link))
        
        self.social_media_layout.addWidget(icon_button)

    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username in accounts and accounts[username] == password:
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.open_chatbot_ui()
            self.close()  # Ferme la fenêtre de connexion
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def open_chatbot_ui(self):
        self.close()
        self.chatbot_ui = ChatBotUI()
        self.chatbot_ui.show()
        

    def open_signup_ui(self):
        if isinstance(self.parent(), MainUI):
            self.parent().switch_to_signup()

class SignUpUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QWidget {
                background: #000000;
                border-radius: 10px;
                padding: 20px;
            }
            QWidget#form_container {
                background: #ffffff;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #444444;
            }
            QLineEdit {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #c41b1c;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #ca3233;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.form_container = QWidget()
        self.form_container.setObjectName("form_container")
        self.form_layout = QVBoxLayout(self.form_container)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)

        self.signup_button = QPushButton("S'inscrire")
        self.signup_button.clicked.connect(self.create_account)
        self.form_layout.addWidget(self.signup_button)

        self.login_button = QPushButton("Déjà un compte ? Se connecter")
        self.login_button.clicked.connect(self.open_login_ui)
        self.form_layout.addWidget(self.login_button)

        self.layout.addWidget(self.form_container)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if username not in accounts:
                accounts[username] = password
                QMessageBox.information(self, "Succès", "Compte créé avec succès !")
                self.open_login_ui()
            else:
                QMessageBox.warning(self, "Erreur", "Nom d'utilisateur déjà existant.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def open_login_ui(self):
        if isinstance(self.parent(), MainUI):
            self.parent().switch_to_login()


class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chatbot d'Alsan Maroc")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add logo at the top
        self.logo_label = QLabel()
        pixmap = QPixmap('images/logo.png')  # Replace with your logo path
        if not pixmap.isNull():
            pixmap = pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")
        self.layout.addWidget(self.logo_label)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: none;
                font-size: 14pt;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
            }
        """)
        self.layout.addWidget(self.chat_display)

        # Input area
        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Tapez votre message ici...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                font-size: 16pt;
                padding: 12px 15px;
                border-radius: 25px;
                border: 1px solid #ddd;
                background-color: #ffffff;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }
        """)
        self.input_layout.addWidget(self.text_input)

        # Send button
        self.send_button = QPushButton("➤")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #c41b1c;
                color: #ffffff;
                border: none;
                font-size: 18pt;
                padding: 12px;
                margin-left: 10px;
                border-radius: 20px;
                width: 50px;
                height: 50px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #ca3233;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        # Initialize Groq API key and client
        self.api_key = os.getenv("GROQ_API_KEY", "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")  # Replace with your valid API key

        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)

    def send_message(self):
        user_message = self.text_input.text()
        if user_message:
            self.display_message("Vous", user_message)
            self.text_input.clear()

            # Get response from Groq API
            bot_response = self.get_groq_response(user_message)
            self.display_message("Bot", bot_response)

    def display_message(self, role, message):
        """Afficher un message dans la zone de discussion avec formatage HTML."""
        if role == "Vous":
            color = "#c41b1c"
            alignment = "right"
            bubble_color = "#e8e8ea"
        else:
            color = "#000000"
            alignment = "left"
            bubble_color = "#e8e8ea"

        formatted_message = self.markdown_to_html(message)
        html_message = f"""
            <div style="text-align: {alignment}; margin-bottom: 10px;">
                <div style="background-color: {bubble_color}; border-radius: 20px; padding: 10px 15px;
                            display: inline-block; max-width: 70%; word-wrap: break-word; color: {color};">
                    <b>{role}:</b> {formatted_message}
                </div>
            </div>
        """
        self.chat_display.append(html_message)

    def get_groq_response(self, message):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur lors de la connexion à l'API Groq: {str(e)}"

    def markdown_to_html(self, text):
        """Convertir le texte formaté en Markdown en HTML simple."""
        text = re.sub(r'^\* (.+)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'^\- (.+)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'\*(.+?)\*', r'<b>\1</b>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<i>\1</i>', text)
        text = text.replace('\n', '<br>')
        if "<li>" in text:
            text = f"<ul>{text}</ul>"
        return text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show the main window which contains Login and Sign Up
    main_window = MainUI()
    main_window.show()
    
    sys.exit(app.exec_())
