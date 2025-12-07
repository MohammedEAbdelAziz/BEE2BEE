ConnectIT
==========

<a href="https://www.producthunt.com/products/connect-it?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-connect&#0045;it" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1016671&theme=neutral&t=1758001359763" alt="Connect&#0032;it&#0032; - Torrent&#0032;Like&#0032;Protocol&#0032;for&#0032;Deployment&#0032;LLM&#0032;Models | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

# ConnectIT

[![PyPI version](https://img.shields.io/pypi/v/connectit.svg)](https://pypi.org/project/connectit/)
[![Python versions](https://img.shields.io/pypi/pyversions/connectit.svg)](https://pypi.org/project/connectit/)
[![Downloads](https://img.shields.io/pypi/dm/connectit.svg)](https://pypi.org/project/connectit/)
[![License](https://img.shields.io/badge/License-Custom-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/connectit/connectit/ci.yml?branch=main)](https://github.com/connectit/connectit/actions)

**A decentralized peer-to-peer network for deploying and accessing AI models.**

ConnectIT allows you to run a node that serves Hugging Face models to the network, or act as a client that automatically discovers and uses the cheapest and fastest model providers available. It features an integrated Supervisor Mode for health monitoring.

## ✨ Features

- 🌐 **Dynamic P2P Network**: Automatically detects your LAN IP and assigns random ports for zero-config setup.
- 👁️ **Supervisor Monitoring**: The API node acts as a "Main Point" that actively monitors peer health (latency, availability) every 60s.
- 🤖 **Async Model Loading**: Loading large models doesn't block the network causing disconnects.
- 💰 **Economic Model**: Set your price per token. Clients automatically route to the best value.
- 🔌 **HTTP API**: REST API to query network status, peers, and health stats.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/loayabdalslam/connectit.chatit.git
cd connectit

# Install with all dependencies
pip install -e .[all]
```

## 🚀 Quick Start

### 1. Start a Supervisor Node (Main Point)

This node will act as the bootstrap server and actively monitor the health of all connected peers.

```bash
# Start on default API port 8000. P2P port can be 4001 or random.
python -m connectit api
```
*The console will show "Supervisor Monitoring Enabled". Check `http://localhost:8000/peers` for health stats.*

### 2. Deploy a Model Provider

Nodes deploy services and join the network. They will be monitored by the Supervisor.

```bash
# Replace bootstrap-link with the Supervisor's link
python -m connectit deploy-hf --model distilgpt2 --bootstrap-link ws://192.168.1.X:4001
```

### 3. Request Generation

```bash
python -m connectit p2p-request "Hello, world!" --model distilgpt2 --bootstrap-link ws://192.168.1.X:4001
```

## 🏗 Architecture

### Supervisor / Main Point
When you run `connectit api`, the node starts a background task (`_monitoring_loop`) that iterates over all connected peers every minute.
-   **Ping**: Sends distinct ping packets to measure RTT.
-   **Health Audit**: Updates the peer's `health_status` (online/degraded) based on connectivity.
-   **API Exposure**: This data is available at `/peers`.

### Core Components
1.  **P2PNode (`p2p_runtime.py`)**: Core engine with gossip, dynamic IP, and monitoring logic.
2.  **Services (`services.py`)**: threaded model loading for stability.
3.  **API (`api.py`)**: FastAPI interface to the node and supervisor stats.

## 🤝 Contributing

We welcome contributions! Please check the [issues](https://github.com/connectit/connectit/issues) page.

## License

Custom License (Non-Commercial). See [LICENSE](LICENSE) for details.
