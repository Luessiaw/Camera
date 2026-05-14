# Capture Manifest

## P0-06 Captures

Capture date: 2026-05-14

Capture interface: `本地连接* 10` / `192.168.137.1` Windows Mobile Hotspot

Capture filter:

```text
host 192.168.137.177
```

Camera:

| Item | Value |
| --- | --- |
| IP | 192.168.137.177 |
| MAC | 58:c5:87:9a:ab:97 |

Phone:

| Item | Value |
| --- | --- |
| IP | 192.168.137.29 |
| MAC | 3a:1c:64:3b:ce:af |

## Raw Capture Files

The raw pcapng files are stored under `01_network_capture/pcap_raw/`.

These files are intentionally ignored by Git because they may contain local network metadata, device identifiers, cloud endpoints, and other sensitive details.

| Scenario | File | Duration | Packets | Size | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| Camera boot with internet access | `20260514_2104_boot_online_camera_192.168.137.177.pcapng` | 120s | 288 | 75416 bytes | Captured power-on, cloud connection, and App preview window |
| App preview video | `20260514_app_preview_camera_192.168.137.177.pcapng` | 60s | 117 | 43360 bytes | Captured App preview traffic while camera was already online |
| App preview video, structured repeat | `20260514_app_preview_structured_camera_192.168.137.177.pcapng` | 90s | 133 | 54148 bytes | Repeated preview capture for P1-04 validation |
| App PTZ control | `20260514_app_ptz_camera_192.168.137.177.pcapng` | 60s | 79 | 31256 bytes | Captured App control scenario; detailed command path still needs P1/P2 analysis |
| App PTZ control, structured repeat | `20260514_app_ptz_structured_camera_192.168.137.177.pcapng` | 120s | 122 | 56704 bytes | Structured PTZ capture for P1-05; manual action annotation pending |

## Initial DNS Observations

These are preliminary observations only. Full DNS/TCP/UDP analysis belongs to P1.

| Domain | Observed Address(es) | Seen In |
| --- | --- | --- |
| `ntp.sjtu.edu.cn` | 17.253.116.253, 17.253.114.43, 17.253.114.35 | boot, preview, PTZ |
| `svc.av380.net` | 120.24.173.70 | boot |
| `alivetype.av380.net` | 8.134.147.2 | boot |
| `alarmserverlist.av380.net` | 219.135.97.79 | boot |
| `devota.av380.net` | 218.91.199.250, 58.221.36.18, 58.221.37.119, 218.91.170.134 | boot, preview |
| `logs.av380.net` | 39.105.177.250 | boot |
| `ipc79.w390.net` | 120.27.12.196 | boot, preview, PTZ |
| `regipc4379.av380.net` | 47.99.1.63 | boot |
| `push2.av380.net` | 118.178.56.123 | boot |

## Initial Conversation Summary

| Scenario | Main Conversations |
| --- | --- |
| Boot online | Camera communicated with `192.168.137.1`, `120.27.12.196`, `120.24.173.70`, `8.134.147.2`, `218.91.199.250`, `58.221.37.119`, `219.135.97.79`, and other external endpoints |
| App preview | Camera communicated with `192.168.137.1`, `218.91.199.250`, `120.27.12.196`, and `17.253.116.253` |
| App PTZ | Camera communicated with `192.168.137.1`, `120.27.12.196`, and `17.253.116.253` |

## P0-06 Result

P0-06 is complete for the initial online, App preview, and App PTZ/control scenarios.

The blocked-internet scenario is intentionally left for P1-06, because it requires changing firewall/DNS behavior and comparing the camera's offline behavior against the baseline captures above.

## Follow-up Analysis

| Stage | File | Notes |
| --- | --- | --- |
| P1-01 | `01_network_capture/boot_capture_analysis.md` | Boot-stage timeline, protocol summary, and main remote conversations |
| P1-02 | `01_network_capture/dns_analysis.md` | DNS domain inventory, observed addresses, and initial endpoint roles |
| P1-03 | `01_network_capture/communication_flow_analysis.md` | TCP/UDP flow summary across boot, preview, and PTZ/control captures |
| P1-04 | `01_network_capture/app_preview_analysis.md` | Structured App preview capture comparison and direct phone-flow check |
| P1-05 | `01_network_capture/app_ptz_analysis.md` | Structured PTZ/control capture analysis; includes local TCP 8800 observation |
