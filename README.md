# SAS-Simulation
Open-source SAS simulator featuring a Python-based sonar image reconstruction and an interactive HTML visualization of underwater echo propagation.

![SAS Simulator Screenshot](sas.png)

[▶️ Watch SAS Simulation Video](SAS-simulator.mp4)

---

# Synthetic Aperture Sonar (SAS) Simulation

This repository includes two components to visualize and understand SAS technology:

## 1. HTML Simulator
A web-based animation that simulates sonar pulse propagation and target detection with visual echo paths and terrain.

**Location:** `html_simulator/index.html`

## 2. Python Simulator
A NumPy + Matplotlib simulation of echo generation and image reconstruction using backprojection.

**Location:** `python_simulator/sas_basic.py`

---

## How to Run

### Python
```bash
pip install numpy matplotlib
python python_simulator/sas_basic.py
