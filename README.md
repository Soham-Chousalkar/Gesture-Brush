# 🎨 Gesture Brush - Virtual Painter

A computer vision-based virtual painting application that allows users to draw on screen using hand gestures captured through a webcam. This project implements advanced hand landmark tracking to create a wireless, touchless digital drawing experience.

![Gesture Brush Demo](GestureBrush_ScreenShots/Screenshot%20(113).png)

## ✨ Features

- **🤚 Advanced Hand Gesture Recognition**: Uses custom hand landmark detection for precise finger tracking
- **🎨 Multiple Drawing Tools**: Draw, Line, Rectangle, Circle, and Erase
- **🌈 Color Selection**: Choose from 5 different colors with intuitive gesture controls
- **⚡ Real-time Drawing**: Create artwork using hand movements with minimal latency
- **🎯 Intuitive Controls**: Point to select tools and colors, use finger gestures for drawing
- **🔧 Python 3.13 Compatible**: Works with the latest Python version

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Webcam
- Good lighting for hand detection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gesture-brush.git
   cd gesture-brush
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # or
   source .venv/bin/activate      # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   cd GestureBrush/Project
   python gesture_brush.py
   ```

## 🎮 Controls

### Hand Gestures
- **Show your hand to the camera**: Basic hand detection
- **Point with index finger**: Move cursor and select tools/colors
- **Index finger up**: Activate drawing mode
- **Index finger down**: Stop drawing
- **Point to top area**: Select drawing tools
- **Point to left area**: Select colors
- **ESC**: Exit application

### Drawing Tools
- **Draw**: Freehand drawing with finger movement
- **Line**: Draw straight lines
- **Rectangle**: Draw rectangles
- **Circle**: Draw circles
- **Erase**: Erase drawn content

## 📁 Project Structure

```
Gesture Brush/
├── GestureBrush/
│   └── Project/
│       ├── gesture_brush.py     # Main application (Python 3.13 compatible)
│       ├── main.py              # Original MediaPipe version
│       ├── demo.py              # Mouse-controlled demo
│       ├── runner.py            # Execution script
│       ├── hand_tracker.py      # Hand tracking module
│       ├── tools.png            # Tool interface
│       └── colors.png           # Color palette
├── GestureBrush_ScreenShots/    # Demo screenshots
├── requirements.txt              # Dependencies
├── README.md                    # This file
└── CHANGELOG.md                 # Project changelog
```

## 🔧 Technical Details

### Hand Landmark Detection
The application uses advanced computer vision techniques to detect hand landmarks:

- **WRIST (0)**: Base reference point
- **INDEX_FINGER_TIP (8)**: Main cursor for drawing
- **MIDDLE_FINGER_TIP (12)**: Secondary finger tracking
- **RING_FINGER_TIP (16)**: Additional finger
- **PINKY_TIP (20)**: Additional finger

### Gesture Recognition
- **Finger Up Detection**: Compares finger tip Y-position with wrist Y-position
- **Tool Selection**: Uses X-coordinate of index finger tip
- **Color Selection**: Uses Y-coordinate of index finger tip
- **Drawing Activation**: Requires index finger to be extended

## 🛠️ Development

### Running Different Versions

1. **Main Application (Recommended)**
   ```bash
   python gesture_brush.py
   ```

2. **Original MediaPipe Version** (Requires Python 3.11/3.12)
   ```bash
   python main.py
   ```

3. **Demo Version** (Mouse-controlled)
   ```bash
   python demo.py
   ```

### Troubleshooting

#### Camera Issues
- Ensure webcam is connected and accessible
- Check camera permissions
- Try different camera index: change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

#### Hand Detection Issues
- Ensure good lighting conditions
- Keep hand clearly visible to camera
- Avoid background objects that might interfere with skin detection

#### Performance Issues
- Reduce camera resolution in the code
- Close other applications using the camera
- Ensure good lighting for hand detection

## 📋 Requirements

- **Python**: 3.13+ (for main version) or 3.11/3.12 (for MediaPipe version)
- **OpenCV**: 4.5.0+
- **NumPy**: 1.19.0+
- **Webcam**: Any standard webcam

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- MediaPipe team for hand tracking inspiration
- All contributors and testers

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the changelog for recent updates

---

**Made with ❤️ for the computer vision community** 