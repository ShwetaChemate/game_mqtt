# Game Notifications System - MQTT Pub/Sub with Django

## 🌟 Overview

This project implements a real-time game notification system using MQTT protocol with Django. Players receive instant updates about game events like starts, pauses, and endings through a publish-subscribe model.

## ✨ Key Features

- **Publisher interface** for game event creators
- **Consumer dashboard** showing player notifications
- **Simple message format**: `prosumio <username> <event>`

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/game-mqtt.git
   cd game-mqtt
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MQTT broker** (default settings):
   ```bash
   brew install mosquitto  # Mac
   sudo apt install mosquitto mosquitto-clients  # Linux
   mosquitto -v  # Start broker in verbose mode
   ```

### Configuration

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

2. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

## 🏃 Running the Application

1. Start Django development server:
   ```bash
   python manage.py runserver
   ```

2. In another terminal, start MQTT client:
   ```bash
   python manage.py mqtt_client
   ```

3. Access the application at:
   - Main page: http://localhost:8000
     
     <img width="417" alt="Screenshot 2025-05-09 at 6 22 25 PM" src="https://github.com/user-attachments/assets/b2ca3b26-5ff5-4ad1-bdc0-b0c31d9df1c5" />

   - Admin: http://localhost:8000/admin

## 🎮 Using the System

### For Game Developers (Publishers)
1. Log in at http://localhost:8000/login
2. Navigate to Publisher dashboard
3. Enter game events in format: `game started`, `level completed`, etc.
   
   <img width="444" alt="Screenshot 2025-05-09 at 6 23 23 PM" src="https://github.com/user-attachments/assets/3a2bbc9e-1eca-4c73-8daa-f36ee90d3bae" />

### For Players (Consumers)
1. Log in with your credentials
2. View real-time notifications at Consumer dashboard
3. Notifications appear in format: `prosumio username event`
   
   <img width="442" alt="Screenshot 2025-05-09 at 6 27 45 PM" src="https://github.com/user-attachments/assets/0809e68d-e3cf-40ea-9b63-14c6617d3f0e" />

