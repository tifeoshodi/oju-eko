Moving from a pitch to a Product Requirements Document (PRD) is exactly how we turn a massive vision into actionable engineering tasks. This document will serve as our internal roadmap for the LBE team and a technical blueprint for proof of our execution plan.

We will strictly scope this PRD to **Phase 1: The Data Collection & Perception MVP**. If we scope too broadly, the project will stall.

Here is the PRD to kick off development.

***

# **Product Requirements Document (PRD)**
## **Project Name:** NORD Pilot (Project "Oju-Eko")
**Phase:** 1 - Data Acquisition & Perception MVP
**Lead Engineer:** Head of AI, Low Budget Engineers (LBE)
**Target Delivery:** 8 Weeks from Hardware Procurement

---

### **1. Product Vision & Objective**
**Vision:** To build the foundational AI perception layer for autonomous driving in unstructured traffic environments (specifically Nigerian roads).
**Phase 1 Objective:** Develop a reliable, portable hardware/software rig capable of recording synchronized, high-framerate sensor data (video, GPS, IMU) across Lagos. Use this data to train a preliminary computer vision model capable of identifying localized hazards (potholes, erratic motorcycles, unregulated pedestrians) with a bounding-box overlay for a client demonstration.

### **2. Target Audience / Stakeholders**
* **Primary Users:** LBE Engineering Team (for data collection and model training).
* **Key Stakeholders:** NORD Motion Executive Team (for evaluating the MVP demonstration).

### **3. Hardware Requirements (The "LBE Starter Pack")**
The physical rig must be non-destructive (no drilling into the vehicle) and easily deployable.
* **Cameras:** 3x USB 3.0 Global Shutter Cameras (e.g., Arducam AR0234).
    * *Config:* 1x Forward Long-Range (60°), 1x Forward Wide-Angle (120°), 1x Rear/Blindspot.
* **Telemetry:** 1x USB IMU + GPS Module (e.g., WitMotion) for spatial logging.
* **Compute:** 1x High-performance laptop equipped with an NVIDIA GPU (RTX 3060+).
* **Storage:** 1x 2TB High-Speed External NVMe SSD (minimum write speed: 1000 MB/s).
* **Power:** 300W DC-to-AC Car Inverter.

### **4. Software & Algorithmic Requirements**
The software stack will be built in Python, focusing on modularity and low-latency execution.

#### **Module A: The Data Logger (`logger.py`)**
* Must capture and synchronize streams from 3 cameras at a minimum of 30 frames per second (FPS) at 1080p resolution.
* Must poll GPS and IMU data and append it to a CSV log, timestamp-matched to the corresponding video frames.
* **Constraint:** Must utilize multi-threading or multi-processing in Python to prevent frame dropping during simultaneous I/O operations.

#### **Module B: The Perception Model (`detector.py`)**
* Utilize an optimized object detection framework (e.g., YOLOv8 or YOLOv10).
* Fine-tune the pre-trained model using the collected "Lagos-v1" dataset.
* **Custom Classes to Train:** `Danfo`, `Okada`, `Keke`, `Pothole`, `Pedestrian`, `Open_Drivable_Space`.

#### **Module C: The Visualizer (`demo.py`)**
* A playback script that takes the raw video files, runs them through the trained model, and outputs a video with colored bounding boxes and confidence scores.
* Must display a dynamic telemetry dashboard overlay (showing speed and G-force impacts from the IMU).

### **5. Success Metrics (KPIs)**
| Metric | Target | Why it Matters |
| :--- | :--- | :--- |
| **Data Synchronization** | < 10ms variance | If camera frames and GPS data are out of sync, the training data is useless. |
| **Capture Stability** | 0 dropped frames | Crucial for capturing sudden movements of motorcycles or sudden braking. |
| **Model Inference Speed** | > 30 FPS on Demo GPU | Proves to NORD that the algorithm can run in real-time on edge hardware. |
| **Dataset Size** | Minimum 50 hours of driving | Required to capture enough edge cases (rain, night, heavy traffic) for a robust demo. |

### **6. Development Milestones**
1.  **Hardware Assembly:** Procure sensors, build the roof mount, and test power stability in a moving car.
2.  **Logger Development:** Write and test the Python script to successfully save timestamped data to the SSD without crashing.
3.  **Data Collection Campaign:** 2 weeks of driving designated routes in Lagos.
4.  **Data Annotation:** Manually label the crucial elements (potholes, Kekes) in a subset of the captured frames.
5.  **Model Fine-Tuning:** Train the YOLO model on the annotated dataset.
6.  **Demo Compilation:** Generate the final video presentation overlaying the AI's "vision" onto the Lagos streets.

***

This PRD gives you a strict perimeter to work within so the team doesn't get distracted by features outside of Phase 1. 

For the very first development step—writing the data logger—how do you want to handle the multi-threading in Python to ensure we can save three heavy 1080p video streams simultaneously without dropping frames?