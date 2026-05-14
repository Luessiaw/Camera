# TCP and UDP Communication Flow Analysis

Stage: P1-03

Source captures:

```text
01_network_capture/pcap_raw/20260514_2104_boot_online_camera_192.168.137.177.pcapng
01_network_capture/pcap_raw/20260514_app_preview_camera_192.168.137.177.pcapng
01_network_capture/pcap_raw/20260514_app_ptz_camera_192.168.137.177.pcapng
```

Camera:

| Item | Value |
| --- | --- |
| IP | 192.168.137.177 |
| MAC | 58:c5:87:9a:ab:97 |
| Gateway | 192.168.137.1 |

## Execution Assessment Before P1-03

No major task-order adjustment is needed.

The current sequence remains valid:

1. P1-01 established that the boot capture contains DHCP, DNS, HTTP, TLS, and UDP cloud traffic.
2. P1-02 identified the primary cloud domains and showed that `ipc79.w390.net` and `devota.av380.net` are the highest-priority endpoints.
3. P1-03 should focus on transport flows, especially `120.27.12.196` and TLS/HTTP endpoints.

Minor interpretation adjustment:

- P1-04 and P1-05 are still useful, but they should be treated as validation/refinement tasks because preview and PTZ baseline captures already exist from P0-06.
- P1-06 should still be delayed until after transport-flow analysis, because blocked-internet testing needs a reliable online baseline.
- P2 should not start yet. No local RTSP/HTTP/ONVIF evidence has appeared in the current traffic.

## High-Level Result

The camera communicates with three categories of endpoints:

| Category | Examples | Transport | Observed Role |
| --- | --- | --- | --- |
| Local gateway/DNS/DHCP | `192.168.137.1` | UDP 53, UDP 67/68, ICMP | Network bootstrapping, DNS, reachability |
| Plain HTTP cloud services | `svc.av380.net`, `alivetype.av380.net`, `alarmserverlist.av380.net`, `logs.av380.net`, `push2.av380.net` | TCP 80/8002/8888/9191/8881 | Service discovery, device alive/type, alarm/push, metadata |
| Encrypted/cloud channel endpoints | `devota.av380.net`, `ipc79.w390.net` | TLS 443, TCP 1340, UDP 8877/9001/7788/1341 | Secure service traffic and persistent/custom IPC cloud traffic |

No direct camera-to-phone LAN data path was identified in the current flow summaries.

## Flow Summary by Scenario

### Boot Online

| Remote | Domain | Protocol/Port | Notes |
| --- | --- | --- | --- |
| `192.168.137.1` | local gateway | DHCP, DNS, ICMP | DHCP Offer/ACK, DNS server, ping target |
| `17.253.116.253` | `ntp.sjtu.edu.cn` chain | UDP 123 | NTP time sync |
| `120.24.173.70` | `svc.av380.net` | TCP 8002 / HTTP | `POST /url/belong`, repeated later |
| `8.134.147.2` | `alivetype.av380.net` | TCP 80 / HTTP | `POST /v1/ipc/alivetype` |
| `219.135.97.79` | `alarmserverlist.av380.net` | TCP 8888 / HTTP | `POST /api/v3/alarm_server_list` |
| `39.105.177.250` | `logs.av380.net` | TCP 9191 / HTTP | `POST /api/v1/dev/meta` |
| `118.178.56.123` | `push2.av380.net` | TCP 8881 / HTTP | `POST /api/v1/detection/alarm` |
| `218.91.199.250`, `58.221.37.119` | `devota.av380.net` | TCP 443 / TLSv1.2 | TLS Client Hello with SNI `devota.av380.net` |
| `120.27.12.196` | `ipc79.w390.net` | TCP 1340, UDP 8877/9001/7788/1341 | Persistent/custom IPC cloud traffic |
| `119.23.22.242` | IP literal HTTP host | TCP 80 / HTTP | HTTP GET with encoded `param` query |

### App Preview

| Remote | Domain | Protocol/Port | Notes |
| --- | --- | --- | --- |
| `120.27.12.196` | `ipc79.w390.net` | TCP 1340, UDP 8877/9001/7788/1341 | Same custom IPC pattern as boot |
| `218.91.199.250` | `devota.av380.net` | TCP 443 / TLSv1.2 | Two short TLS sessions with SNI `devota.av380.net` |
| `17.253.116.253` | `ntp.sjtu.edu.cn` chain | UDP 123 | NTP |
| `192.168.137.1` | local gateway | DNS, DHCP | DNS and DHCP traffic |

No HTTP request was identified in this preview capture.

### App PTZ/Control

| Remote | Domain | Protocol/Port | Notes |
| --- | --- | --- | --- |
| `120.27.12.196` | `ipc79.w390.net` | TCP 1340, UDP 8877/9001/7788/1341 | Same custom IPC pattern appears during control scenario |
| `17.253.116.253` | `ntp.sjtu.edu.cn` chain | UDP 123 | NTP |
| `192.168.137.1` | local gateway | DNS, DHCP, ICMP | DNS/DHCP and ping-related traffic |

No direct camera-to-phone PTZ flow was identified in the high-level summary.

## `ipc79.w390.net` / `120.27.12.196` Flow Pattern

This endpoint appears in boot, preview, and PTZ/control captures.

Observed ports:

| Protocol | Port | Pattern |
| --- | ---: | --- |
| TCP | 1340 | Very short TCP handshake followed by immediate FIN/close |
| UDP | 1341 | Short 16-byte outbound packet near TCP 1340 setup |
| UDP | 9001 | Short 16-byte request and 16-byte response |
| UDP | 7788 | 64-byte outbound packet and 16-byte response |
| UDP | 8877 | Repeated request/response, then periodic keepalive-like packets |

Observed repeated behavior:

- A short TCP `1340` session opens and closes quickly.
- UDP `1341` and `9001` fire near the TCP session.
- UDP `7788` sends a larger 64-byte packet and receives a 16-byte reply.
- UDP `8877` then becomes the dominant recurring flow.
- During preview and PTZ captures, UDP `8877` repeats every few seconds at first, then roughly every 10 seconds.

Interpretation:

- `120.27.12.196` is likely a core cloud-side IPC endpoint.
- UDP `8877` likely carries keepalive, registration, relay, or control-channel traffic.
- The repeated appearance in PTZ/control makes this endpoint the best candidate for later control-path analysis.
- The observed packets are small and not obviously standard RTP/RTSP video packets.

## Plain HTTP Flows

| Domain / Remote | Port | Method / Path | Observed Purpose |
| --- | ---: | --- | --- |
| `svc.av380.net` / `120.24.173.70` | 8002 | `POST /url/belong` | Service routing / region lookup |
| `alivetype.av380.net` / `8.134.147.2` | 80 | `POST /v1/ipc/alivetype` | Device alive/type registration |
| `alarmserverlist.av380.net` / `219.135.97.79` | 8888 | `POST /api/v3/alarm_server_list` | Alarm/push server list |
| `logs.av380.net` / `39.105.177.250` | 9191 | `POST /api/v1/dev/meta` | Device metadata/log report |
| `push2.av380.net` / `118.178.56.123` | 8881 | `POST /api/v1/detection/alarm` | Detection/alarm report |
| `119.23.22.242` | 80 | `GET /?param=<base64-like value>` | Unknown HTTP lookup with encoded parameter |

Interpretation:

- These endpoints expose useful plaintext service paths.
- They should be useful for later firmware analysis and cloud-disable planning.
- They do not look like local video streaming endpoints.

## TLS Flows

| Domain | Remote(s) | Port | Notes |
| --- | --- | ---: | --- |
| `devota.av380.net` | `58.221.37.119`, `218.91.199.250` | 443 | TLSv1.2, SNI visible |

Interpretation:

- Payload is encrypted.
- The endpoint appears during boot and preview.
- Role is not proven from transport alone; likely secure vendor service, config, OTA, or related device cloud traffic.

## Local LAN / Phone Relationship

Observed local addresses:

| Address | Role |
| --- | --- |
| `192.168.137.1` | Windows hotspot gateway/DNS/DHCP |
| `192.168.137.177` | Camera |
| `192.168.137.29` | Phone |

No direct camera-to-phone TCP or UDP conversation was identified in the current summaries.

Interpretation:

- App preview/control likely depends on vendor cloud relay or cloud-mediated coordination.
- This does not yet rule out a hidden local service on the camera; P2 port scanning is still required later.

## P1-03 Result

P1-03 is complete.

Remote IPs, ports, and broad protocol types have been identified. The most important follow-up target is:

```text
ipc79.w390.net / 120.27.12.196
```

Next recommended tasks:

1. P1-04: repeat/validate App preview capture and compare whether traffic volume or timing changes during preview.
2. P1-05: repeat/validate PTZ control capture with a more structured action script: left, right, up, down, stop, each with timestamps.
3. P1-06: block public internet and observe whether any local service remains available.
