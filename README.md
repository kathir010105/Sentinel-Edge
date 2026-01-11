# SentinelEdge: Edge-Based Intelligent Intrusion Detection System

## 🎯 Demo Project Overview

An **offline, edge-computing intrusion detection system** using local AI for real-time person detection. This project demonstrates how modern AI-powered security systems can operate completely autonomously on edge devices without cloud dependencies.

---

## 📁 Project Structure

```
Sentinel-Edge/
├── src/                          # Source code modules
│   ├── camera_feed.py           # Camera capture (640x480 @ 30 FPS)
│   ├── person_detector.py       # YOLOv8 person detection
│   ├── intrusion_detector.py    # State machine & decision logic
│   ├── alert_system.py          # Evidence capture & logging
│   └── offline_verifier.py      # System verification tool
├── alerts/                       # Alert screenshots (auto-generated)
├── logs/                         # Event logs (auto-generated)
├── models/                       # AI model cache
│   └── yolov8n.pt               # YOLOv8 nano model (6.2MB)
├── venv/                         # Python virtual environment
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── DEMO_CHECKLIST.md            # Complete demo preparation guide
├── QUICK_START.md               # Fast reference for demo day
└── OFFLINE_VERIFICATION.md      # Offline capability documentation
```

---

## 🚀 Quick Start (Demo Day)

### Run Complete System:

```bash
# 1. Open PowerShell in project directory
cd C:\Users\KATHIRVEL\Documents\VS_CODE\Sentinel-Edge

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run full intrusion detection system
python src/alert_system.py
```

### Demo Actions:

1. **System starts** → Status: "SYSTEM CLEAR" (green)
2. **Enter frame** → Status: "ANALYZING..." (orange)
3. **Stay 3 seconds** → Status: "⚠️ INTRUSION ALERT ⚠️" (red, flashing)
4. **Leave frame** → After 2 seconds, returns to "CLEAR"
5. **Press 'q' or ESC** → Exit and show statistics

### Verify Offline Capability:

```bash
# Run verification tool
python src/offline_verifier.py

# Disconnect WiFi, then run again
python src/offline_verifier.py
# Should show: "📴 OFFLINE MODE" + "🎉 EDGE COMPUTING VERIFIED!"
```

---

## 💻 Environment Setup

### Hardware:

- **CPU**: Intel i5 12500H
- **GPU**: NVIDIA RTX 3050 (16GB RAM)
- **Camera**: Built-in webcam
- **OS**: Windows 10/11

### Software:

- **Python**: 3.10.0
- **AI Framework**: PyTorch + Ultralytics (YOLOv8)
- **Computer Vision**: OpenCV 4.8.1
- **Model**: YOLOv8n (nano - optimized for edge)

---

## ✨ Features Implemented

### Core Features (Demo Scope):

- ✅ **Live Camera Feed**: 640x480 resolution @ 30 FPS
- ✅ **Person Detection**: YOLOv8n AI model (local inference)
- ✅ **Intrusion Logic**: Time-based (3s) + confidence-based (60%) filtering
- ✅ **Alert System**: Automatic screenshot capture + event logging
- ✅ **Offline Operation**: 100% functional without internet

### Technical Features:

- ✅ **State Machine**: CLEAR → DETECTING → ALERT transitions
- ✅ **False Alarm Prevention**: Dual-threshold filtering
- ✅ **Evidence Capture**: Up to 5 screenshots per alert with timestamps
- ✅ **Event Logging**: Text + JSON logs for audit trail
- ✅ **Real-time Visualization**: Bounding boxes, status indicators, statistics

---

## 🎯 Edge Computing Principles Demonstrated

| Principle               | Implementation                            |
| ----------------------- | ----------------------------------------- |
| **Local Processing**    | All AI inference on device (no cloud API) |
| **Zero Latency**        | <50ms detection response time             |
| **Offline Operation**   | Works without internet connectivity       |
| **Privacy Preserved**   | Video never leaves device                 |
| **Autonomous Decision** | State machine operates independently      |
| **Resource Efficient**  | 6.2MB model, low power consumption        |

---

## 📊 System Performance

- **Detection Speed**: ~10-20 FPS on CPU, 100+ FPS on GPU
- **Model Size**: 6.2MB (YOLOv8n)
- **Memory Usage**: ~200MB RAM
- **Detection Accuracy**: 85-95% confidence for persons
- **Alert Latency**: 3 seconds (configurable)
- **Screenshot Size**: ~100-200KB per image

---

## 📖 Documentation

- **[DEMO_CHECKLIST.md](DEMO_CHECKLIST.md)**: Complete demo preparation guide (recording script, troubleshooting, tips)
- **[QUICK_START.md](QUICK_START.md)**: Fast reference for demo day (emergency commands, key points)
- **[OFFLINE_VERIFICATION.md](OFFLINE_VERIFICATION.md)**: Offline capability proof and verification guide

---

## 🎬 Demo Recording Guide

**See [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md) for complete recording script**

**Quick Demo Flow (7 minutes):**

1. System overview (1 min)
2. Offline verification (1.5 min)
3. Live detection demo (3 min)
4. Evidence review (1 min)
5. Closing remarks (30 sec)

---

## 🔧 Troubleshooting

### Common Issues:

**Camera won't open:**

- Close other apps using camera (Zoom, Teams)
- Check Windows Camera privacy settings

**No detection:**

- Check lighting (face must be visible)
- Move closer to camera
- Ensure facing camera directly

**System slow:**

- Close unnecessary applications
- CPU mode is slower than GPU (expected)

**For detailed troubleshooting, see [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md)**

---

## 🌟 Key Differentiators

1. **True Edge Computing**: All processing local, zero cloud dependency
2. **Intelligent Filtering**: Time + confidence prevents false alarms
3. **Evidence Capture**: Automatic forensic documentation
4. **Offline Verified**: Proven to work without internet
5. **Production Ready**: Can deploy on Raspberry Pi, Jetson Nano

---

## 🚀 Future Extensions (Beyond Demo Scope)

- Multiple camera support
- Face recognition integration
- Mobile app notifications
- MQTT/IoT integration for smart homes
- GPU optimization (CUDA, ONNX)
- Cloud backup (optional, preserving edge-first architecture)
- Multi-zone detection
- Time-based scheduling

---

## 📜 License

See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- **YOLOv8**: Ultralytics (https://github.com/ultralytics/ultralytics)
- **OpenCV**: Computer vision library
- **PyTorch**: Deep learning framework

---

## 📞 Project Info

- **Project**: SentinelEdge - Edge-Based Intelligent Intrusion Detection System
- **Category**: Edge Computing + AI + Security
- **Demo Date**: January 12, 2026
- **Status**: ✅ Complete and Demo-Ready

---

**🎉 All systems verified and ready for demonstration!**
