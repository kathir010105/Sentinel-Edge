# SentinelEdge - Final Demo Checklist

## 🎯 Demo Date: Day After Tomorrow (January 12, 2026)

## 📹 Format: Recorded Video Demo

---

## ✅ PRE-DEMO CHECKLIST (Complete Before Recording)

### 1. System Verification (Run 24 Hours Before Demo)

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run complete system verification
python src/offline_verifier.py
```

**Expected Result:**

```
✓ CAMERA: PASS
✓ MODEL: PASS
✓ DETECTION: PASS
✓ ALERTS: PASS
✓ FRAMEWORK: PASS
Overall Status: ✓ ALL SYSTEMS READY
```

❌ **If ANY component fails**: Fix immediately, don't wait for demo day!

---

### 2. Test Run (1 Hour Before Recording)

**Complete System Test:**

```bash
python src/alert_system.py
```

**Test Checklist:**

- [ ] Camera opens successfully
- [ ] Your face is detected (red bounding box appears)
- [ ] Stay for 3+ seconds → Alert triggers (red flashing)
- [ ] Screenshots saved to `alerts/` folder
- [ ] Logs written to `logs/` folder
- [ ] System returns to CLEAR when you leave
- [ ] Press 'q' to exit cleanly

**Expected Time:** System should trigger alert in exactly 3 seconds

---

### 3. Clean Up Old Test Data (Optional)

**To start fresh for recording:**

```bash
# Delete old screenshots
Remove-Item alerts\*.jpg

# Delete old logs (CAREFUL!)
Remove-Item logs\intrusion_log.txt
Remove-Item logs\intrusion_log.json
```

⚠️ **Warning**: Only do this if you want a clean recording. Keep existing files if you want to show system history.

---

### 4. Camera & Environment Setup

**Camera Position:**

- [ ] Webcam at eye level
- [ ] Face clearly visible in frame
- [ ] Good lighting (face not too dark/bright)
- [ ] No backlighting (avoid window behind you)

**Environment:**

- [ ] Clean background (minimize distractions)
- [ ] Quiet room (for narration)
- [ ] Close unnecessary applications
- [ ] Disable notifications (Windows Focus Assist)

**Screen Setup:**

- [ ] Resolution: 1920x1080 recommended
- [ ] Taskbar visible (shows time, WiFi status)
- [ ] VS Code closed or minimized
- [ ] PowerShell terminal ready

---

### 5. Recording Software Setup

**Recommended Tools (Pick One):**

- **OBS Studio** (Free, powerful): https://obsproject.com/
- **Windows Game Bar** (Built-in): Win+G
- **Loom** (Easy, web-based): https://loom.com/

**Recording Settings:**

- [ ] Resolution: 1920x1080 (Full HD)
- [ ] FPS: 30 (matches camera feed)
- [ ] Audio: Microphone enabled for narration
- [ ] Include system audio (optional)

---

## 🎬 DEMO RECORDING SCRIPT (5-7 Minutes)

### Opening (30 seconds)

**Screen**: Desktop with terminal ready

**Script**:

> "Hello, I'm presenting SentinelEdge - an Edge-Based Intelligent Intrusion Detection System using Embedded AI. This system demonstrates how AI-powered security can run completely on local devices without cloud dependencies, ensuring privacy, zero latency, and autonomous operation."

---

### Part 1: System Overview (1 minute)

**Screen**: Show project folder structure in VS Code or File Explorer

**Script**:

> "SentinelEdge consists of four main components:
>
> 1. Camera Feed - captures live video at 640x480 resolution
> 2. Person Detector - uses YOLOv8, a lightweight AI model optimized for edge devices
> 3. Intrusion Logic - implements time-based and confidence-based filtering to prevent false alarms
> 4. Alert System - captures evidence and logs events locally
>
> All of this runs on my laptop without any internet connection."

**Show**: Folders (src/, alerts/, logs/, models/)

---

### Part 2: Offline Verification (1.5 minutes)

**Screen**: Terminal

**Commands**:

```bash
# Show you're online
python src/offline_verifier.py
```

**Script**:

> "First, let me verify the system while online. As you can see, all components pass verification. Now watch as I disconnect from the internet..."

**Action**:

- Click WiFi icon in taskbar
- Disconnect from WiFi (SHOW THIS CLEARLY)

**Commands**:

```bash
# Verify offline
python src/offline_verifier.py
```

**Script**:

> "With the internet disconnected, the system still passes all checks. This proves true edge computing - all AI processing happens locally on this device."

---

### Part 3: Live Detection Demo (3 minutes)

**Screen**: Terminal → SentinelEdge window

**Commands**:

```bash
python src/alert_system.py
```

**Script**:

> "Now I'll run the complete intrusion detection system. Notice the WiFi is still disconnected - everything you're about to see happens entirely offline."

**Wait for system to start, then**:

**Demo Sequence:**

1. **Initial State (10 seconds)**

   - Show camera feed
   - Status: "SYSTEM CLEAR" (green)
   - **Script**: "The system is monitoring. Currently, no persons detected."

2. **Detection Phase (3 seconds)**

   - Move into frame
   - Status changes to "ANALYZING..." (orange)
   - Progress bar shows 0% → 100%
   - **Script**: "I'm now in frame. The system detects me but requires continuous presence for 3 seconds before triggering an alert. This prevents false alarms from people briefly passing by."

3. **Alert Triggered (5-10 seconds)**

   - Status: "⚠️ INTRUSION ALERT ⚠️" (red, flashing)
   - Red bounding box around you
   - Alert ID displayed
   - Screenshots being saved (watch terminal messages)
   - **Script**: "Alert triggered! Notice the flashing red status, bounding box around me, and the system is automatically capturing screenshots for evidence. All of this is happening in real-time on this device."

4. **Clear State (3 seconds)**

   - Move out of frame
   - Wait 2 seconds
   - Status returns to "SYSTEM CLEAR"
   - **Script**: "When I leave the frame, the system automatically clears the alert after 2 seconds and returns to monitoring mode."

5. **Exit**
   - Press 'q'
   - Show statistics in terminal
   - **Script**: "The system has processed [X] frames and triggered [Y] alerts. Let me show you the evidence captured..."

---

### Part 4: Evidence Review (1 minute)

**Screen**: File Explorer

**Show**:

1. **Navigate to `alerts/` folder**

   - Show timestamped screenshots
   - Open 1-2 images to display
   - **Script**: "Here are the screenshots captured during the alert. Each image is timestamped and shows the detected person with confidence scores."

2. **Navigate to `logs/` folder**
   - Open `intrusion_log.txt` in Notepad
   - Show log entries
   - **Script**: "The system also maintains detailed logs of all events with timestamps, confidence scores, and alert durations. This provides a complete audit trail."

---

### Closing (30 seconds)

**Screen**: Return to desktop, reconnect WiFi (optional)

**Script**:

> "SentinelEdge demonstrates the power of edge computing for security applications. By processing everything locally, we achieve:
>
> - Zero latency for real-time detection
> - Complete privacy - no data sent to cloud servers
> - Zero ongoing costs - no cloud subscription fees
> - Reliable operation even without internet connectivity
>
> This system can be deployed on embedded devices like Raspberry Pi or NVIDIA Jetson for production use. Thank you for watching."

---

## 📊 TALKING POINTS (If Asked Questions)

### Technical Questions:

**Q: Why YOLOv8?**

> "YOLOv8n (nano variant) is optimized for edge devices - only 6.2MB, fast inference, and excellent accuracy. It's the industry standard for real-time object detection on resource-constrained devices."

**Q: How does it prevent false alarms?**

> "Two-layer filtering: First, time-based - must detect person continuously for 3 seconds. Second, confidence-based - average confidence must exceed 60%. This combination virtually eliminates false positives."

**Q: Can it run on Raspberry Pi?**

> "Yes! The current implementation uses PyTorch, which works on Raspberry Pi 4. For even better performance, we can use ONNX runtime or TensorFlow Lite for embedded deployment."

**Q: What about multiple people?**

> "The system detects multiple people simultaneously. Each person gets their own bounding box, and the alert triggers if ANY person exceeds the 3-second threshold."

**Q: Battery life on embedded devices?**

> "YOLOv8n is very efficient. On a Raspberry Pi 4, it consumes about 3-5W during active detection. With a 10,000mAh battery, you could run for 6-8 hours continuously."

### Edge Computing Questions:

**Q: What makes this edge computing vs. just offline?**

> "Edge computing means processing data WHERE it's generated, not WHERE it's stored. We're not just saving bandwidth - we're making decisions autonomously at the edge with sub-50ms latency."

**Q: What if the edge device fails?**

> "In production, you'd have multiple edge nodes or edge-to-edge synchronization. For this demo, we're showing a single-node edge system, but the architecture scales horizontally."

---

## 🐛 TROUBLESHOOTING GUIDE

### Problem: Camera doesn't open

**Symptoms**: "Cannot access camera" error

**Solutions**:

1. Close other apps using camera (Zoom, Teams, Skype)
2. Check Windows Camera privacy settings
3. Try different camera ID:
   ```python
   # In src/camera_feed.py or alert_system.py
   camera = CameraFeed(camera_id=1)  # Try 1 instead of 0
   ```

---

### Problem: "Model not found"

**Symptoms**: "yolov8n.pt not found" error

**Solutions**:

1. Check if file exists: `ls yolov8n.pt`
2. Re-download model:
   ```bash
   python src/person_detector.py
   ```
3. Verify internet connection during download

---

### Problem: No detection / detection not working

**Symptoms**: No bounding boxes appear when you're in frame

**Solutions**:

1. Check lighting (face must be visible)
2. Lower confidence threshold:
   ```python
   # In src/alert_system.py
   detector = PersonDetector(model_name='yolov8n.pt', confidence_threshold=0.3)
   ```
3. Move closer to camera
4. Ensure you're facing the camera

---

### Problem: Alert triggers too quickly/slowly

**Symptoms**: Alert behavior not as expected

**Solutions**:

1. Adjust detection threshold:
   ```python
   # In src/alert_system.py
   intrusion_detector = IntrusionDetector(
       detection_threshold_seconds=2.0,  # Change from 3.0 to 2.0
       confidence_threshold=0.5,          # Lower if needed
       clear_timeout_seconds=1.0          # Adjust clear time
   )
   ```

---

### Problem: System is slow/laggy

**Symptoms**: Low FPS, delayed responses

**Solutions**:

1. Close other applications
2. Lower camera resolution (already 640x480, shouldn't need this)
3. Increase wait time: Change `cv2.waitKey(1)` to `cv2.waitKey(10)` in alert_system.py
4. Note: CPU mode is slower than GPU - this is expected

---

### Problem: Screenshots not saving

**Symptoms**: No files in `alerts/` folder

**Solutions**:

1. Check folder exists: `ls alerts/`
2. Check permissions
3. Verify disk space
4. Look for error messages in terminal

---

## 🎓 PRESENTATION TIPS

### Do's:

✅ **Speak clearly and confidently**
✅ **Show enthusiasm for edge computing**
✅ **Explain WHY each decision was made**
✅ **Demo offline capability prominently**
✅ **Show actual evidence files**
✅ **Keep demo under 7 minutes**
✅ **Practice 2-3 times before recording**

### Don'ts:

❌ Don't apologize for CPU mode (it's intentional for demo)
❌ Don't spend too long on code (focus on functionality)
❌ Don't skip the offline verification (it's your key differentiator)
❌ Don't mumble or rush through talking points
❌ Don't record in one take if it doesn't go well (re-record!)

---

## 📋 FINAL PRE-RECORDING CHECKLIST

**30 Minutes Before Recording:**

- [ ] Run system verification
- [ ] Test complete demo flow
- [ ] Clean up test data (optional)
- [ ] Check camera lighting
- [ ] Close unnecessary apps
- [ ] Disable notifications
- [ ] Prepare recording software
- [ ] Test audio levels

**Right Before Recording:**

- [ ] Take a deep breath
- [ ] Smile (you got this!)
- [ ] Check camera framing
- [ ] Start recording software
- [ ] Begin demo script

**After Recording:**

- [ ] Review recording (watch entire video)
- [ ] Check audio quality
- [ ] Verify all features shown
- [ ] Re-record if needed
- [ ] Export/save final video

---

## 🎯 SUCCESS CRITERIA

Your demo is successful if you show:
✅ Live camera feed working
✅ Real-time person detection with bounding boxes
✅ State machine transitions (CLEAR → DETECTING → ALERT)
✅ Offline operation (WiFi disconnected)
✅ Screenshot capture and evidence storage
✅ Event logging
✅ Clean system exit

---

## 📦 SUBMISSION CHECKLIST

Before submitting:

- [ ] Video file exported (MP4 recommended)
- [ ] Video length: 5-7 minutes
- [ ] Audio clear and audible
- [ ] All features demonstrated
- [ ] Offline capability shown
- [ ] Evidence files shown
- [ ] File size reasonable (<500MB)

---

## 🚀 YOU'RE READY!

You have built:

- ✅ Live camera feed
- ✅ Local AI person detection
- ✅ Intelligent intrusion logic
- ✅ Alert system with evidence capture
- ✅ Complete offline capability
- ✅ Professional documentation

**This is a complete, competition-ready edge computing demo!**

Good luck with your presentation! 🎉

---

**Last Updated**: January 10, 2026, 10:30 PM
**Demo Date**: January 12, 2026 (Night)
**Status**: All systems ready for recording
