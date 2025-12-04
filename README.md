# Mercury - Intelligent Customer Support Triage System

Mercury is an AI-powered customer support triage agent designed to streamline ticket management. It analyzes incoming customer complaints, categorizes them, assesses sentiment and urgency, and drafts an appropriate response using the Groq Llama 3 API.


## 🚀 Features

-   **Automated Triage**: Instantly categorizes tickets (e.g., Billing Dispute, Hardware Defect).
-   **Sentiment Analysis**: Detects customer emotion (e.g., Frustrated, Neutral).
-   **Urgency Scoring**: Prioritizes tickets based on severity (Low to Critical).
-   **Draft Responses**: Generates context-aware replies for support agents.
-   **Modern UI**: Clean, responsive dashboard built with Next.js and Tailwind CSS.

## 🛠️ Tech Stack

-   **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide React.
-   **Backend**: FastAPI, Python 3.10+, LangChain (Groq).
-   **AI Model**: Llama 3 (via Groq API).
-   **Containerization**: Docker & Docker Compose.

## 📋 Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   A [Groq API Key](https://console.groq.com/keys).

## 🚀 Quick Start (Docker)

The easiest way to run Mercury is using Docker Compose.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/UMer438/Mercury-Intelligent-Customer-Support-Triage-System.git
    cd Mercury-Intelligent-Customer-Support-Triage-System
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the `backend` directory and add your Groq API Key.
    ```bash
    # backend/.env
    GROQ_API_KEY=your_groq_api_key_here
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker compose up --build
    ```

4.  **Access the Application:**
    -   **Frontend**: Open [http://localhost:3000](http://localhost:3000)
    -   **Backend API Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔧 Manual Installation (Local Development)

If you prefer to run the services locally without Docker:

### Backend

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up `.env` as shown above.
5.  Run the server:
    ```bash
    python main.py
    ```

### Frontend

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
