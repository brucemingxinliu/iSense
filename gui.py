import sys
import subprocess
from PyQt6 import QtWidgets, QtGui, QtCore
import os

class ImageMatcherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('iSense V1.0')
        self.setFixedSize(800, 500)

        # Set up the interface
        self.layout = QtWidgets.QVBoxLayout(self)

        # Input fields for image paths with default text
        self.input_layout = QtWidgets.QHBoxLayout()
        self.left_image_path_input = QtWidgets.QLineEdit(self)
        self.left_image_path_input.setPlaceholderText("Enter path for left image")
        self.left_image_path_input.setText('templates/left.jpg')  # Default path for left image

        self.right_image_path_input = QtWidgets.QLineEdit(self)
        self.right_image_path_input.setPlaceholderText("Enter path for right image")
        self.right_image_path_input.setText('templates/right.jpg')  # Default path for right image

        self.input_layout.addWidget(self.left_image_path_input)
        self.input_layout.addWidget(self.right_image_path_input)
        self.layout.addLayout(self.input_layout)

        # Display images
        self.images_layout = QtWidgets.QHBoxLayout()

        self.label_left = QtWidgets.QLabel()
        self.label_left.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_left.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.label_right = QtWidgets.QLabel()
        self.label_right.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_right.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.images_layout.addWidget(self.label_left)
        self.images_layout.addWidget(self.label_right)

        self.layout.addLayout(self.images_layout)

        # Button to run the subprocesses
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.clicked.connect(self.run_matchers)
        self.layout.addWidget(self.run_button)

        # Label to show the combined score
        self.score_label = QtWidgets.QLabel("")
        self.score_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.score_label)

    def set_image(self, label, image_path):
        if not os.path.isfile(image_path):
            label.setText(f"Image not found: {os.path.basename(image_path)}")
            return

        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            label.setText("Failed to load image.")
        else:
            scaled_pixmap = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

    def run_matchers(self):
        left_image_path = self.left_image_path_input.text()
        right_image_path = self.right_image_path_input.text()

        if not os.path.isfile(left_image_path):
            QtWidgets.QMessageBox.warning(self, "Input Error", f"Left image path is invalid: {left_image_path}")
            return
        if not os.path.isfile(right_image_path):
            QtWidgets.QMessageBox.warning(self, "Input Error", f"Right image path is invalid: {right_image_path}")
            return

        left_result_path = 'result/left_result.jpg'
        right_result_path = 'result/right_result.jpg'

        try:
            left_result = subprocess.run(
                ['python3', 'l_match.py', left_image_path, 'templates/ltemp.jpg', left_result_path],
                capture_output=True, text=True, check=True
            )
            right_result = subprocess.run(
                ['python3', 'r_match.py', right_image_path, 'templates/rtemp.jpg', right_result_path],
                capture_output=True, text=True, check=True
            )

            print("Left Script Output:", left_result.stdout.strip())
            print("Right Script Output:", right_result.stdout.strip())

            left_score = float(left_result.stdout.strip())
            right_score = float(right_result.stdout.strip())

            combined_score = left_score + right_score
            print("Combined Score:", combined_score)

            result_text = "NG - 质量不通过" if combined_score < 0.94 else f"PASS - Combined Score: {combined_score:.2f}"
            self.score_label.setText(result_text)

            # Ensure the images are updated
            self.set_image(self.label_left, left_result_path)
            self.set_image(self.label_right, right_result_path)

        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Execution Error", f"An error occurred: {e.stderr}")
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Result Error", f"Could not parse scores: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImageMatcherApp()
    window.show()
    sys.exit(app.exec())