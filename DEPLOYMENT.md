# ConnectIT Deployment Guide

## Can I use Vercel?
**Short Answer: No.**

**Reason:** Vercel is designed for *Serverless Functions* and Static Websites.
-   **No WebSockets**: `connectit` requires a persistent WebSocket connection to keep the P2P node alive. Vercel functions time out after 10-60 seconds, which will disconnect your node immediately.
-   **No Background Tasks**: The P2P node runs in the background. Serverless functions freeze immediately after sending a HTTP response.

---

## Recommended Deployment Options (Cloud)

Since `connectit` needs to run as a **Service** (a long-running process), you should use platforms that support Docker or persistent apps.

### 1. Railway (Easiest)
Railway detects the `Dockerfile` automatically.
1.  Push your code to GitHub.
2.  Import project in [Railway.app](https://railway.app/).
3.  Add a generic variable `PORT=4002` (FastAPI).
4.  Railway will build and deploy.
5.  **Note**: For P2P to work best, you might need a service that allows exposing multiple ports (TCP/UDP), or just rely on the main HTTP/WS port.

### 2. Fly.io (Best for P2P)
Fly.io supports persistent VMs and is great for networking.
1.  Install `flyctl`.
2.  Run `fly launch`.
3.  It will use the `Dockerfile`.
4.  Run `fly deploy`.

### 3. VPS (DigitalOcean / AWS / Hetzner)
You can rent a small server ($5/mo) and run:
```bash
# 1. Install Docker
curl -fsSL https://get.docker.com | sh

# 2. Build & Run
docker build -t connectit .
docker run -d --net=host --restart=always connectit
```
*Note: `--net=host` is recommended for P2P apps to simplify port forwarding.*

## Local Deployment (Home)
If running at home (as you are now):
-   **UPnP**: The app tries to open ports automatically.
-   **Manual**: Forward TCP port `4003` on your router to your PC.
-   **Tunnel**: Use `ngrok` if you cannot access your router.
