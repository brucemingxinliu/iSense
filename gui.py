import sys
import subprocess
from PyQt6 import QtWidgets, QtGui, QtCore

class ImageMatcherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Matcher')
        
        # Fixed window size
        self.setFixedSize(800, 500)

        # Set up the interface
        self.layout = QtWidgets.QVBoxLayout(self)

        # Input fields for image paths
        self.input_layout = QtWidgets.QHBoxLayout()
        self.left_image_path_input = QtWidgets.QLineEdit(self)
        self.left_image_path_input.setPlaceholderText("Enter path for left image")
        self.right_image_path_input = QtWidgets.QLineEdit(self)
        self.right_image_path_input.setPlaceholderText("Enter path for right image")

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
        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            label.setText("Image not found")
        else:
            scaled_pixmap = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

    def run_matchers(self):
        # Get image paths from input fields
        left_image_path = self.left_image_path_input.text()
        right_image_path = self.right_image_path_input.text()

        # Result image paths
        left_result_path = 'result/left_result.jpg'
        right_result_path = 'result/right_result.jpg'

        # Run subprocesses for the left and right matchers
        left_process = subprocess.run(['python3', 'l_match.py', left_image_path, left_result_path], capture_output=True, text=True)
        right_process = subprocess.run(['python3', 'r_match.py', right_image_path, right_result_path], capture_output=True, text=True)

        # Set the result images in the top window
        self.set_image(self.label_left, left_result_path)
        self.set_image(self.label_right, right_result_path)

        try:
            # Fetch scores from the outputs
            left_score = float(left_process.stdout.strip())
            right_score = float(right_process.stdout.strip())

            # Calculate the combined score
            combined_score = left_score + right_score

            # Update the GUI with the combined score
            if combined_score < 0.8:
                result_text = "NG"
            else:
                result_text = f"OK - Combined Score: {combined_score:.2f}"

            self.score_label.setText(result_text)

        except ValueError:
            self.score_label.setText("Error calculating scores")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImageMatcherApp()
    window.show()
    sys.exit(app.exec())