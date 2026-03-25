---
name: offline-deploy
description: "Provision Raspberry Pi devices with local AI (TinyLlama), pre-loaded curriculum, WiFi hotspot, and sync capabilities for offline learning hubs."
metadata:
  source: ekatra
  version: 1.0.0
---

# Offline Deploy

Set up Raspberry Pi learning hubs for areas without internet connectivity.

## Input

You need:
- **Device**: Raspberry Pi 5 or Orange Pi (ARM SBC, recommended 4GB+ RAM)
- **Course content**: Pre-generated course JSON and flashcard decks
- **Deployment location**: Site details (power availability, expected learner count,
  connectivity for periodic sync)
- **Admin credentials**: SSH key for remote management via Tailscale

## Process

### Step 1 — Flash base image

1. Flash Raspberry Pi OS Lite (64-bit) to SD card
2. Enable SSH, set hostname to `ekatra-<site-code>`
3. Configure locale and timezone for deployment location
4. Set up auto-login for the ekatra service user

### Step 2 — Install software stack

Core services:
- **Python 3.11+** with Flask for the learning server
- **Ollama** for local model inference
- **TinyLlama** (or Phi-3-mini) model — download and verify checksum
- **SQLite** for learner data storage
- **hostapd + dnsmasq** for WiFi hotspot

Install and configure:
```
ekatra-offline/
  main.py          — Flask server (routes: /, /admin, /generate, /health)
  src/             — Model manager, WiFi manager, curriculum loader
  config/          — Device-specific configuration
  static/          — Frontend assets for admin dashboard
  templates/       — HTML templates for client chat and admin UI
```

### Step 3 — Configure WiFi hotspot

1. Set SSID to `Ekatra-Learn-<site-code>`
2. Configure WPA2 password
3. Set IP range for connected clients (192.168.4.x)
4. Configure DHCP lease time (2 hours)
5. Set up captive portal redirect to learning interface

### Step 4 — Pre-load curriculum

1. Import course JSON files into SQLite database
2. Load quiz banks and flashcard decks
3. Pre-generate common Q&A responses for the course topic
4. Verify all content is accessible via `/` endpoint

### Step 5 — Configure monitoring

Set up local monitoring:
- `/health` — Service health check
- `/api/system/stats` — CPU, RAM, disk, temperature, uptime
- `/api/clients/active` — Connected devices (IP-based tracking)
- `/api/wifi/status` — Hotspot status, connected client count
- Client inactivity timeout: 5 minutes

### Step 6 — Configure remote access

1. Install Tailscale VPN client
2. Register device on the Ekatra Tailscale network
3. Set up SSH key-based authentication
4. Configure data sync script (runs when internet detected):
   - Push: learner progress, quiz responses, interaction logs
   - Pull: updated course content, model updates, configuration changes
5. Test remote access: `ssh ekatra@<device>.tail-net`

### Step 7 — Deployment verification

Run full verification:
- [ ] WiFi hotspot broadcasts and accepts connections
- [ ] Learning interface loads on connected phone browser
- [ ] AI Q&A generates responses (TinyLlama inference)
- [ ] Admin dashboard shows system stats
- [ ] Client tracking registers connected devices
- [ ] Tailscale VPN connects (if internet available)
- [ ] Power draw is within budget (8-10W for solar viability)

## Output

- Provisioned device ready for field deployment
- Device manifest: hostname, Tailscale IP, site code, admin password hash,
  pre-loaded courses, model version
- Deployment checklist: all verification points passed
- Site handover document: power requirements, WiFi range, max concurrent clients,
  support contact procedure

## Maintenance

- **Monthly**: Check disk usage, update model if newer version available
- **Quarterly**: Rotate admin credentials, audit learner data retention
- **On-demand**: Remote troubleshooting via Tailscale SSH, log retrieval
