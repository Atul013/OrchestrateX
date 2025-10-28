# OrchestrateX

OrchestrateX is an advanced multi-model collaborative AI system designed to deliver higher-quality and dynamically refined responses through real-time multi-model critique and feedback. It intelligently selects the best model to answer a user prompt while simultaneously engaging other models as critics to improve the answer on the fly.

---

## Features

- **Multi-Model Selection:** Intelligently chooses the most suitable model from a pool of GLM4.5, GPT-OSS, Llama 4 Maverick, MoonshotAI Kimi, Qwen3, and TNG DeepSeek R1T2 Chimera to generate the initial response.
- **Collaborative Criticism:** Other models provide real-time critiques and suggestions to enhance the output of the answering model.
- **Dynamic Refinement:** The answering model iteratively refines its output based on feedback.
- **API Key Rotation:** Automatic rotation of API keys across multiple providers for reliability and rate limit management.
- **High Output Quality:** Combines strengths of multiple AI models to produce superior results.
- **Modern React UI:** Clean, responsive interface for seamless interaction with the orchestration system.

---

## How It Works

1. **User Prompt:** A user submits a request (e.g., "Build the landing page for my portfolio website").
2. **Model Selection:** OrchestrateX selects the best model to generate the initial response.
3. **Critique Loop:** Other models evaluate the response in real-time, providing constructive feedback.
4. **Refinement:** The main responding model updates its output based on critiques.
5. **Final Output:** The user receives a highly refined and collaboratively enhanced answer.

---

## Architecture

**Backend:**
- Flask API with Google Cloud Firestore integration
- Multi-model orchestration engine
- Automatic API key rotation system
- Rate limiting and request management

**Frontend:**
- React-based chat interface
- Real-time model response display
- Multi-model critique visualization

**Deployment:**
- Docker containerization
- Google Cloud Run compatible
- CI/CD with Cloud Build

---

## Why OrchestrateX?

- **Maximizes Answer Quality:** Leverages complementary strengths across multiple AI models
- **Real-Time Collaboration:** Multi-agent feedback and learning in real-time
- **Transparency & Trust:** Detailed critique and collaboration visible to users
- **Production-Ready:** Clean architecture with automated deployment pipelines
- **Scalable Infrastructure:** Built for cloud deployment with automatic scaling

---

## Getting Started

### Prerequisites
```bash
# Python 3.8+
# Node.js 18+
# Docker (optional)
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Atul013/OrchestrateX.git
   cd OrchestrateX
   ```

2. **Set up environment variables:**
   ```bash
   cp orche.env.example orche.env
   # Add your API keys to orche.env
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**
   ```bash
   cd FRONTEND/CHAT\ BOT\ UI/ORCHACHATBOT/project
   npm install
   ```

5. **Run the backend:**
   ```bash
   python working_api.py
   ```

6. **Run the frontend:**
   ```bash
   npm run dev
   ```

### Docker Deployment

```bash
docker build -t orchestratex .
docker run -p 8080:8080 --env-file orche.env orchestratex
```

### Google Cloud Deployment

```bash
gcloud builds submit --config cloudbuild.yaml
```

---

## Technology Stack

**Backend:**
- Python 3.8+ with Flask
- Google Cloud Firestore
- OpenRouter API integration

**Frontend:**
- React with TypeScript
- Vite build system
- Modern CSS with responsive design

**Infrastructure:**
- Docker containerization
- Google Cloud Run
- Cloud Build CI/CD

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For inquiries, contributions, or support, please open an issue on GitHub.

---

**OrchestrateX** — Harnessing the power of multiple AI models to deliver better, faster, and smarter responses.
