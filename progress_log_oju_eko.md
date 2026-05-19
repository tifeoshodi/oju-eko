# **Engineering Log Book: Project "Oju-Eko"**
**Version:** 1.0
**Project Lead:** Low Budget Engineers (LBE)
**Goal:** Perception MVP for Autonomous Driving in Nigerian Traffic

---

## **1. Environment Setup & Diagnostics**
| Date | Action | Outcome |
| :--- | :--- | :--- |
| 24-Apr-2026 | Initial System Check | Detected CARLA 0.9.15 on Windows with Python 3.11. Identified Version Mismatch between 0.9.16 client and 0.9.15 server. |
| 24-Apr-2026 | Hardware Stress Test | Identified critical VRAM bottleneck. `LowLevelFatalError` in `PixelReader` confirmed hardware cannot support heavy 3D rendering (Town10). |
| 24-Apr-2026 | Port Configuration | Successfully confirmed CARLA listener on Port 2000 using `-nullrhi` mode. |

---

## **2. Custom Python Environment (The "Software Fix")**
Due to CARLA 0.9.15 supporting only up to Python 3.10, a custom environment was built to bypass system-level incompatibilities.
*   **Build Target:** Python 3.10.20 (Source: `Python-3.10.20.tar.xz`).
*   **Compilation:** Built using MSVC 2022 Build Tools (`PCbuild/build.bat`).
*   **Library Installation:**
    *   `carla 0.9.15`: Installed via PyPI (specifically compatible with CP310).
    *   `pygame 2.6.1`: Required for manual control and visualization.
    *   `numpy 2.2.6`: Backend for sensor data processing.
    *   `ultralytics`: AI framework for YOLO object detection.
*   **Executable Path:** `c:\Users\user\Downloads\CARLA_0.9.15\Python-3.10.20\PCbuild\amd64\python.exe`

---

## **3. Project Oju-Eko Initiation**
*   **PRD Finalized:** Defined **Phase 1: Data Acquisition & Perception MVP**.
*   **Designated Classes:** `Danfo`, `Okada`, `Keke`, `Pothole`, `Pedestrian`.
*   **Architecture Decision:** Switched to a **Simulation Bridge** using `Town01` for logic testing while hardware rig is in procurement.

---

## **4. Software Modules Developed**
### **Module A: Data Logger (`logger.py`)**
*   **Status:** Functional Prototype.
*   **Architecture:** Multi-processing (Independent processes for `front_long`, `front_wide`, `rear`, and `telemetry`).
*   **Constraint:** Resolution set to 640x480 for stability on current hardware.

### **Module B: Perception Engine (`detector.py`)**
*   **Status:** Initialized.
*   **Model:** YOLOv8 Nano (`yolov8n.pt`) integrated.
*   **Validation:** Inference confirmed successful on mock frames.

---

## **5. Current Technical Blockers & Workarounds**
*   **Blocker:** `EXCEPTION_ACCESS_VIOLATION` in CARLA rendering thread when sensors are active.
*   **Root Cause:** Incompatibility between rendering hardware interface and the simulator's pixel-reading pipeline on this specific GPU.
*   **Workaround:** Development shifted to "Offline Perception"—building the logic using static frames and mock data generators while bypassing live CARLA camera rendering.

---

## **6. Next Steps**
1.  **Dashboard Development**: Create `demo.py` to simulate the colored bounding box overlay on recorded footage.
2.  **Dataset Acquisition**: Begin gathering real-world images of Nigerian vehicles to initiate "Lagos-v1" annotation.
3.  **Hardware Sync**: Map local IMU/GPS serial data into the `logger.py` CSV format.

***
*End of Log v1.0*
