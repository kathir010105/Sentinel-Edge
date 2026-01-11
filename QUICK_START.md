# SentinelEdge - Quick Start Guide

## 🚀 DEMO DAY - QUICK REFERENCE

**Copy this to your phone or print it out for easy reference during demo!**

---

## ⚡ FASTEST PATH TO DEMO (2 Minutes)

### 1. Open Terminal

Press `Win + X` → Select "PowerShell"

### 2. Navigate to Project

```bash
cd C:\Users\KATHIRVEL\Documents\VS_CODE\Sentinel-Edge
```

### 3. Activate Environment

```bash
.\venv\Scripts\Activate.ps1
```

### 4. Run Complete System

```bash
python src/alert_system.py
```

### 5. Demo Actions

- **CLEAR**: System monitoring (green)
- **Enter frame**: Stay for 3 seconds
- **ALERT**: Red flashing (screenshots auto-save)
- **Exit**: Press 'q' or ESC

---

## 📋 FULL DEMO SEQUENCE

### Preparation (2 minutes before recording)

```bash
# 1. Open terminal
cd C:\Users\KATHIRVEL\Documents\VS_CODE\Sentinel-Edge
.\venv\Scripts\Activate.ps1

# 2. Test verification
python src/offline_verifier.py

# 3. Close unnecessary apps
```

### Recording Flow (7 minutes)

**Part 1: Intro** (30 sec)

- Introduce project
- Show folder structure

**Part 2: Offline Verification** (1.5 min)

```bash
# With WiFi ON
python src/offline_verifier.py

# Disconnect WiFi (show taskbar)

# With WiFi OFF
python src/offline_verifier.py
```

**Part 3: Live Demo** (3 min)

```bash
# Still offline!
python src/alert_system.py

# Actions:
# - Show CLEAR state
# - Enter frame → DETECTING
# - Wait 3 seconds → ALERT
# - Leave frame → CLEAR
# - Press 'q' to exit
```

**Part 4: Evidence** (1 min)

```bash
# Show screenshots
explorer alerts

# Show logs
notepad logs\intrusion_log.txt
```

**Part 5: Closing** (30 sec)

- Summarize edge computing benefits
- Thank viewers

---

## 🎯 KEY COMMANDS

| Action           | Command                          |
| ---------------- | -------------------------------- |
| Activate venv    | `.\venv\Scripts\Activate.ps1`    |
| Verify system    | `python src/offline_verifier.py` |
| Run full demo    | `python src/alert_system.py`     |
| Test camera only | `python src/camera_feed.py`      |
| Test detection   | `python src/person_detector.py`  |
| Show alerts      | `explorer alerts`                |
| Show logs        | `explorer logs`                  |

---

## 🎤 KEY TALKING POINTS

### 1. Opening

> "SentinelEdge - Edge-Based Intelligent Intrusion Detection using Embedded AI"

### 2. Edge Computing Definition

> "Processing data WHERE it's generated, not in the cloud"

### 3. Offline Capability

> "Everything runs locally - zero internet required after setup"

### 4. Detection Logic

> "3-second threshold prevents false alarms"

### 5. Evidence Capture

> "Automatic screenshot and logging for forensics"

### 6. Benefits

> "Zero latency, complete privacy, no ongoing costs"

---

## ⚠️ EMERGENCY FIXES

### Camera won't open

```bash
# Try different camera ID
# Edit src/alert_system.py line ~30
# Change: camera = CameraFeed(camera_id=1)
```

### Not detecting you

- Check lighting (face visible)
- Move closer to camera
- Face the camera directly

### System too slow

- Close other applications
- Task Manager → End unnecessary processes

### Alert won't trigger

- Stay in frame for full 3 seconds
- Don't move too much
- Check confidence threshold (should be 0.5-0.6)

---

## 📊 WHAT TO SHOW IN VIDEO

✅ **MUST SHOW:**

1. Offline verification (WiFi disconnect)
2. Live detection with bounding boxes
3. Alert triggering (red flashing)
4. Screenshots in alerts/ folder
5. Event logs

✅ **NICE TO HAVE:**

- Code walkthrough (brief)
- Statistics at end
- Multiple alert cycles

❌ **SKIP:**

- Long code explanations
- Installation process
- Debugging/troubleshooting

---

## 🎬 RECORDING CHECKLIST

**Before Recording:**

- [ ] Camera lighting good
- [ ] Background clean
- [ ] Notifications disabled
- [ ] Other apps closed
- [ ] Script ready
- [ ] Recording software ready

**During Recording:**

- [ ] Speak clearly
- [ ] Show WiFi disconnect clearly
- [ ] Stay in frame for 3+ seconds
- [ ] Show evidence files
- [ ] Keep under 7 minutes

**After Recording:**

- [ ] Watch entire video
- [ ] Check audio quality
- [ ] Verify all features shown
- [ ] Re-record if needed

---

## 💡 PRO TIPS

1. **Practice 2-3 times** before final recording
2. **Disconnect WiFi visibly** (show taskbar)
3. **Speak with confidence** (you built this!)
4. **Show timestamps** on screenshots
5. **Keep moving** (don't stay silent)
6. **Smile** (it shows in your voice)

---

## 🆘 LAST-MINUTE ISSUES

### If system completely broken:

1. Don't panic
2. Check [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md) troubleshooting section
3. Re-run verification: `python src/offline_verifier.py`
4. Restart laptop if needed (last resort)

### If camera not working:

- Use phone as webcam (DroidCam, EpocCam)
- Or focus on recorded footage

### If running out of time:

- Skip offline verification (less impressive but okay)
- Focus on live detection
- Must show: detection working + evidence files

---

## 📞 SUPPORT (If Needed)

**Self-Help:**

1. Check [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md) (detailed guide)
2. Check [OFFLINE_VERIFICATION.md](OFFLINE_VERIFICATION.md) (offline proof)
3. Re-run: `python src/offline_verifier.py`

**Common Issues:**

- Camera: Close other apps using it
- Model: Re-download with `python src/person_detector.py`
- Detection: Check lighting and distance

---

## ✅ FINAL CHECK (5 Min Before Recording)

Run these commands:

```bash
cd C:\Users\KATHIRVEL\Documents\VS_CODE\Sentinel-Edge
.\venv\Scripts\Activate.ps1
python src/offline_verifier.py
python src/alert_system.py
```

If all work → **YOU'RE READY TO RECORD!** 🎉

---

## 🎯 SUCCESS = SHOWING THESE 6 THINGS

1. ✅ Camera feed with live detection
2. ✅ Bounding boxes around persons
3. ✅ Alert triggers after 3 seconds
4. ✅ Works OFFLINE (WiFi disconnected)
5. ✅ Screenshots saved automatically
6. ✅ Logs created with timestamps

**If you show all 6, your demo is a SUCCESS!**

---

**Good luck! You've got this! 🚀**

---

**Emergency Commands:**

```bash
# If stuck, restart from here:
cd C:\Users\KATHIRVEL\Documents\VS_CODE\Sentinel-Edge
.\venv\Scripts\Activate.ps1
python src/alert_system.py
```
