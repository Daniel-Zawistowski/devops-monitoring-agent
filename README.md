# DevOps Monitoring Agent 🚀

## 📖 Overview
A lightweight, modular monitoring daemon built in Python. Designed to continuously observe system health (CPU, RAM, Disk space) and perform HTTP health checks on critical service endpoints. It features real-time alerting via Discord Webhooks, ensuring high availability and rapid incident response for infrastructure.

## ✨ Key Features & Architecture
* **Modular Design:** Strict separation of concerns with a dedicated Orchestrator (`main_agent.py`), hardware metrics collector, and network health checker.
* **Single Source of Truth (SSOT):** Centralized configuration management using environment variables.
* **Resilience & Failsafes:** Built-in exception handling (e.g., `NameResolutionError` catching) and intelligent webhook validation to prevent daemon crashes during network partitions.
* **Clean Code Principles:** Extensively refactored to eliminate redundancy (DRY), utilizing dynamic path resolution and Type Hinting.
* **Real-time Alerting:** Instant Slack/Discord notifications for critical threshold breaches and HTTP anomalies (e.g., 404/500 errors).

## ⚙️ Prerequisites
To run this project, you need:
* Python 3.x
* Docker & Docker Compose (optional)
* Discord Webhook URL

## 🚀 How to Run (Local)

1. Clone the repository:
\`\`\`bash
git clone https://github.com/Daniel-Zawistowski/devops-monitoring-agent.git
cd devops-monitoring-agent
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Set Environment Variables and Run:
\`\`\`bash
export WEBHOOK_URL="your_discord_webhook_here"
export CHECK_INTERVAL="60"
python3 main_agent.py
\`\`\`

## 🐳 How to Run (Docker)

1. Build the Docker image:
\`\`\`bash
docker build -t monitoring-agent .
\`\`\`

2. Run the container in detached mode (-d) with environment variables:
\`\`\`bash
docker run -d \
  -e WEBHOOK_URL="your_discord_webhook_here" \
  -e CHECK_INTERVAL="60" \
  monitoring-agent
\`\`\`