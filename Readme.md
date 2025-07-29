# 🤖 BUGGI – AI-Powered Healthcare Monitoring Assistant

## 📌 Project Overview

**BUGGI** is an innovative AI-powered healthcare assistant developed as a final-year project at the University of AU, recognized as the **Best College Project** for its novel approach to health monitoring. It seamlessly integrates wearable health devices and manual inputs with an intelligent backend to provide **personalized health alerts, medication reminders, and daily wellness insights** via **WhatsApp**, enhancing accessibility for users of all ages.

**New Idea**: BUGGI introduces a **hybrid health data input system**, combining wearable data with manual inputs and a **context-aware AI** that adapts insights based on user demographics and regional health trends, making it a pioneering solution in personalized healthcare.

---

## 🚀 Features

### 🩺 Real-Time Health Monitoring
- Collects metrics (heart rate, steps, SpO2, etc.) via **Google Fit API**
- Supports **manual health data entry** for non-wearable users

### 💬 WhatsApp-Based Notifications
- Delivers daily health reports, alerts, and medication reminders using **WhatsApp Cloud API**

### 🔐 Secure Authentication & Device Integration
- Implements **Google Sign-In** for secure user authentication and wearable syncing

### 📊 AI-Driven Health Analytics
- Machine learning model for:
  - Anomaly detection in health metrics
  - Predictive risk assessment for chronic conditions
  - Personalized wellness recommendations

### ☁️ Scalable Cloud Infrastructure
- Secure data storage on **Firebase / Google Cloud**
- Robust **Django-based backend** with RESTful API

---

## 🧠 AI Model Specifications

- Trained on anonymized datasets (heart rate, steps, SpO2, etc.)
- Real-time anomaly detection for health irregularities
- Predictive analytics for chronic conditions (e.g., hypertension, diabetes)
- Context-aware insights tailored to user profiles

---

## 📚 Technology Stack

| Layer            | Technology                    |
|------------------|-------------------------------|
| Frontend         | React.js, Tailwind CSS        |
| Backend          | Django (Python)               |
| APIs             | Google Fit API, WhatsApp Cloud API |
| Cloud            | Firebase, Google Cloud Storage |
| Database         | SQLite (Development), PostgreSQL (Production) |
| Authentication   | Google Sign-In                |

---

## 🔧 Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ThulasiRaman03778/BUGGI-AI-Assist.git
cd BUGGI-AI-Assist
```

### 2. Set Up Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
```



### 3. Configure Environment Variables
Create a `.env` file in the root directory with the following:

```env
GOOGLE_FIT_CLIENT_ID=your_client_id
GOOGLE_FIT_CLIENT_SECRET=your_client_secret
WHATSAPP_API_TOKEN=your_token
DJANGO_SECRET_KEY=your_django_secret
FIREBASE_CREDENTIALS=your_firebase_credentials_json
```

### 4. Run the Application

#### Backend:
```bash
python manage.py runserver
```


---

## 🔄 Future Enhancements

- 🌐 **Multilingual Support**: Add regional language support for WhatsApp notifications
- 📲 **Expanded Wearable Compatibility**: Integrate with brands like boAt, Noise, and Boult
- 💉 **Advanced Chronic Disease Prediction**: Enhanced models for blood pressure, diabetes, and sleep analysis
- 🏥 **EMR and Hospital Integration**: Enable seamless data exchange with healthcare providers
- 📈 **Gamified Wellness Incentives**: Introduce rewards for achieving health goals

---

## 📸 Sample Output

**WhatsApp Notification Example**:
```text
🩺 Daily Health Summary (29 Jul 2025)
👣 Steps: 6,400
❤️ Heart Rate: 72 bpm (Normal)
🫁 SpO2: 97%
💊 Reminder: Blood Pressure Medication at 8:00 AM

✅ No anomalies detected. Stay active and hydrated!
```

---

## 📄 License

```text
MIT License

Copyright (c) 2025 Thulasi Raman S

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📬 Contact Information

For inquiries, collaborations, or feedback, contact:

📧 **thulasiraman03778@email.com**  
🌐 **University of AU Final Year Project**: Best College Project Award 2025

---

## 🌟 Contributions

Contributions are encouraged! For major changes, please open an issue to discuss proposed enhancements. Fork the repository and submit pull requests for review.
