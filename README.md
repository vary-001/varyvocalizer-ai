aryVocalizer (VVZ) 🎵
Neural Audio Isolation Engine v4
Isolate vocals with surgical precision using Hybrid Transformer Demucs architecture.
![alt text](./frontend/public/vary-vocalizer.png)
📖 Overview
VaryVocalizer is a production-grade Music Source Separation application. It uses deep learning models to deconstruct audio files into their constituent stems (Vocals and Instrumentals).
Unlike standard scripts, VVZ is built on an Asynchronous Event-Driven Architecture, allowing it to handle heavy audio processing in the background while providing a smooth, interactive "Glassmorphism" UI to the user.
✨ Key Features
HT-Demucs v4 Model: State-of-the-art separation quality.
Asynchronous Processing: Celery + Redis queue management prevents server timeouts.
Interactive Mixer: Real-time muting/soloing of stems using Wavesurfer.js.
Focus Mode: "MyVocal" feature to instantly isolate the vocal track for karaoke or analysis.
Modern UI: Brutalist/Minimalist design with Framer Motion animations and dynamic backgrounds.
Dockerized: One command setup for the entire stack.
📸 Screenshots
The Dashboard	The Mixer
![alt text](./frontend/public/ui.png)
![alt text](./frontend/public/vary-vocalizer.png)
Clean, file-drop interface	Interactive waveform manipulation
🏗 Architecture
The app follows a Microservices pattern orchestrated by Docker Compose.
code
Mermaid
graph TD
    Client[Next.js Frontend] -->|Upload MP3| API[FastAPI Backend]
    API -->|Save File| Storage[Local/S3]
    API -->|Push Job ID| Redis[Redis Queue]
    
    Worker[Celery Worker] -->|Listen| Redis
    Worker -->|Process Audio| Demucs[AI Model]
    Demucs -->|Save Stems| Storage
    
    Client -->|Poll Status| API
    Client -->|Download| Storage
The Stack
Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS, Framer Motion.
Backend: Python 3.10, FastAPI, Uvicorn.
AI Engine: PyTorch, Torchaudio, Demucs (Facebook Research), FFmpeg.
Task Queue: Celery, Redis (Broker).
DevOps: Docker, Docker Compose.
🚀 Getting Started
Prerequisites
Docker and Docker Compose installed.
(Optional) NVIDIA GPU with CUDA drivers (for faster processing).
Installation
Clone the repository
code
Bash
git clone https://github.com/your-username/vary-vocalizer.git
cd vary-vocalizer
Environment Setup
The default configuration works out of the box. However, you can check backend/app/config.py for storage paths.
Run with Docker (Recommended)
This will build the Python backend, the AI worker, and the Node.js frontend.
code
Bash
docker compose up --build
Note: The first run will take time as it downloads PyTorch (2GB+) and the Demucs models.
Access the App
Frontend: http://localhost:3000
Backend API: http://localhost:8000/docs
📂 Project Structure
code
Text
vary-vocalizer/
├── docker-compose.yml       # Orchestrator for Web, Worker, Redis, Frontend
├── backend/                 # Python API & AI Logic
│   ├── app/
│   │   ├── main.py          # FastAPI Entry Point
│   │   ├── tasks.py         # The "Chef" (AI Processing Logic)
│   │   ├── worker.py        # Celery Configuration
│   │   └── api.py           # Route Handlers
│   ├── storage/             # Volume for separated audio
│   ├── requirements.txt     # Python Dependencies
│   └── Dockerfile           # Backend Container
│
└── frontend/                # Next.js UI
    ├── src/
    │   ├── app/             # Page Routes
    │   ├── components/      # UI Components (AudioMixer, UploadCard)
    │   └── lib/             # API Connectors
    ├── public/              # Static Assets (Images, Logos)
    └── Dockerfile           # Frontend Container
🤝 For Collaborators: Roadmap & Improvements
We welcome contributions! Here are the current priorities to take VVZ to the next level:
1. 🧹 Automated Cleanup (High Priority)
Issue: Currently, separated files stay in storage forever.
Task: Implement a scheduled task (Celery Beat) in backend/app/tasks.py to delete files older than 1 hour.
2. ⚡ GPU Acceleration
Issue: The Docker container currently defaults to CPU.
Task: Update docker-compose.yml to pass NVIDIA runtime flags so the AI runs 10x faster.
3. 📱 Mobile Responsiveness
Issue: The AudioMixer waveform canvas can be squashed on small screens.
Task: Refine CSS in src/components/AudioMixer.tsx to handle responsive resizing gracefully.
4. 🔒 User Authentication
Task: Add Supabase or NextAuth to allow users to save their library of separated songs.
🛠 Development Commands
If you want to run services individually (without Docker) for debugging:
Backend (Terminal 1):
code
Bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
Worker (Terminal 2):
code
Bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
Frontend (Terminal 3):
code
Bash
cd frontend
npm run dev
📄 License
This project is open-source.
Code: MIT License.
AI Models: Demucs is released under the MIT license by Meta Research.
