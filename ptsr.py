import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract

class OCRApp(QMainWindow):
    def __init__(self):
        super(OCRApp, self).__init__()

        # Tambahkan baris ini untuk konfigurasi PyTesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('OCR App')

        # Create a central widget as a QWidget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout for the central widget
        vbox = QVBoxLayout(central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Drag and drop or open an image.")
        vbox.addWidget(self.image_label)

        self.btn_open = QPushButton('Open Image', self)
        self.btn_open.clicked.connect(self.open_image)
        vbox.addWidget(self.btn_open)

        self.btn_ocr = QPushButton('Perform OCR', self)
        self.btn_ocr.clicked.connect(self.perform_ocr)
        vbox.addWidget(self.btn_ocr)

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

    def perform_ocr(self):
        if hasattr(self, 'image_label'):
            pixmap = self.image_label.pixmap()
            if pixmap:
                image_path = "temp_image.png"
                pixmap.save(image_path)

                try:
                    text = pytesseract.image_to_string(Image.open(image_path))
                    print("OCR Result:")
                    print(text)
                except Exception as e:
                    print(f"Error during OCR: {e}")

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        urls = mime_data.urls()

        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        urls = mime_data.urls()

        if urls and urls[0].scheme() == 'file':
            file_path = urls[0].toLocalFile()
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            event.acceptProposedAction()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ocr_app = OCRApp()
    ocr_app.show()
    sys.exit(app.exec_())
