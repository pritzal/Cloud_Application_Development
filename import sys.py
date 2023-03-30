import sys
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.web = QWebEngineView()
        self.web.load(QUrl('https://www.google.com')) # Set default URL here
        self.web.show()

        self.url_bar = QLineEdit()
        self.url_bar.setText('https://www.google.com') # Set default URL here

        self.go_button = QPushButton('Go')
        self.go_button.clicked.connect(self.go_to_url)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.url_bar)
        button_layout.addWidget(self.go_button)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.web)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def go_to_url(self):
        url = self.url_bar.text()
        if url.startswith('http'):
            self.web.load(QUrl(url))
        else:
            self.web.load(QUrl('http://' + url))

class Worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        print("Worker started")
        self.signal.emit("Task started")
        # Your time-consuming web-related task goes here
        for i in range(5):
            self.signal.emit(f"Task in progress: {i}")
            QTimer.singleShot(1000, lambda: None) # Simulate a time-consuming task
        self.signal.emit("Task completed")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()

    worker = Worker()
    worker.signal.connect(lambda msg: browser.status_label.setText(msg))
    worker.start()

    sys.exit(app.exec_())
