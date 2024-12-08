echo "Updating package lists..."
sudo apt update

echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

pip install opencv-python
pip install matplotlib
pip install PyQt5
pip install Pillow
pip install numpy
pip install --upgrade Pillow

echo "Installation Complete!"