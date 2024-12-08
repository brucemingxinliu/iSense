import sys
import subprocess
from PyQt6 import QtWidgets, QtGui, QtCore

class ImageMatcherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Matcher')
        self.setGeometry(100, 100, 800, 400)
        self.setFixedSize(800, 400)
        # Set up the interface
        self.layout = QtWidgets.QVBoxLayout(self)

        # Display images
        self.images_layout = QtWidgets.QHBoxLayout()
        
        # Define default image paths
        self.left_image_path = 'templates/left.jpg'
        self.right_image_path = 'templates/right.jpg'
       
        # Result image paths
        self.left_result_path = 'result/right_result.jpg'
        self.right_result_path = 'result/left_result.jpg'

        self.label_left = QtWidgets.QLabel("Left Image")
        self.label_left.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_left.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.label_right = QtWidgets.QLabel("Right Image")
        self.label_right.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_right.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.set_image(self.label_left, self.left_image_path)
        self.set_image(self.label_right, self.right_image_path)

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
        if QtGui.QPixmap(image_path).isNull():
            print(f"Could not load image from path: {image_path}")
            label.setText("Image not found")
            return
        pixmap = QtGui.QPixmap(image_path)
        # Scale the pixmap to fit the label
        scaled_pixmap = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # Re-scale images when the widget size changes
        self.set_image(self.label_left, self.left_image_path)
        self.set_image(self.label_right, self.right_image_path)
        super().resizeEvent(event)

    def run_matchers(self):
        # Run subprocesses for each image processing task
        subprocess.run(['python3', 'l_match.py', self.left_image_path, self.left_result_path], check=True)
        subprocess.run(['python3', 'r_match.py', self.right_image_path, self.right_result_path], check=True)

        # After subprocesses complete, load and update the images in the labels
        self.set_image(self.label_left, self.left_result_path)
        self.set_image(self.label_right, self.right_result_path)

        # Score processing (this is just an example, actual implementation may vary)
        # Assume score is returned and printed from l_match.py and r_match.py
        left_score_process = subprocess.run(['python3', 'l_match.py', '--score'], capture_output=True, text=True)
        right_score_process = subprocess.run(['python3', 'r_match.py', '--score'], capture_output=True, text=True)

        # Assuming that each script prints a single number as its score
        try:
            left_score = float(left_score_process.stdout.strip())
            right_score = float(right_score_process.stdout.strip())

            # Calculate the combined score
            combined_score = left_score + right_score
            print(combined_score)
            # Update the GUI
            if combined_score < 0.8:
                result_text = "NG"
            else:
                result_text = f"OK - Combined Score: {combined_score:.2f}"

            self.score_label.setText(result_text)


        except ValueError as e:
            self.score_label.setText("Error calculating scores")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImageMatcherApp()
    window.show()
    sys.exit(app.exec())