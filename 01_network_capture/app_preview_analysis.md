# App Preview Traffic Analysis

Stage: P1-04

Source captures:

```text
01_network_capture/pcap_raw/20260514_app_preview_camera_192.168.137.177.pcapng
01_network_capture/pcap_raw/20260514_app_preview_structured_camera_192.168.137.177.pcapng
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

## Capture Summary

| Capture | Duration | Packets | Size | Notes |
| --- | ---: | ---: | ---: | --- |
| `20260514_app_preview_camera_192.168.137.177.pcapng` | 60s | 117 | 43360 bytes | Initial App preview baseline |
| `20260514_app_preview_structured_camera_192.168.137.177.pcapng` | 90s | 133 | 54148 bytes | Structured repeat capture: close/reopen preview and keep live view |

## Structured Preview Capture Findings

Main IPv4 conversations:

| Remote | Packets | Bytes | Notes |
| --- | ---: | ---: | --- |
| `58.221.36.18` | 55 | about 12 kB | `devota.av380.net` TLS traffic |
| `192.168.137.1` | 45 | about 34 kB | Gateway, DNS, DHCP, and local ICMP/ping-related traffic |
| `120.27.12.196` | 28 | 2084 bytes | `ipc79.w390.net`, TCP 1340 and UDP custom traffic |
| `17.253.116.125` | 2 | 180 bytes | NTP |

DNS observed:

| Domain | Address(es) |
| --- | --- |
| `ipc79.w390.net` | `120.27.12.196` |
| `ntp.sjtu.edu.cn` | `17.253.116.125`, `17.253.114.35`, `17.253.116.253` |
| `devota.av380.net` | `58.221.36.18`, `58.221.37.119`, `218.91.170.134`, `218.91.199.250` |

TLS observed:

| Domain | Remote | Port | Notes |
| --- | --- | ---: | --- |
| `devota.av380.net` | `58.221.36.18` | 443 | TLSv1.2 Client Hello with SNI `devota.av380.net`; two short sessions |

Custom IPC/cloud flow observed:

| Remote | Protocol/Port | Pattern |
| --- | --- | --- |
| `120.27.12.196` | TCP 1340 | Short handshake and close |
| `120.27.12.196` | UDP 1341 | Short outbound packet near TCP 1340 setup |
| `120.27.12.196` | UDP 9001 | Short request/response |
| `120.27.12.196` | UDP 7788 | 64-byte outbound packet, 16-byte response |
| `120.27.12.196` | UDP 8877 | Repeated keepalive-like traffic |

## Phone Direct-Traffic Check

Filter used:

```text
ip.addr == 192.168.137.29
```

Result:

- No packets involving the phone IP were present in the camera-filtered structured preview capture.
- No direct camera-to-phone TCP or UDP flow was identified.

Interpretation:

- The App preview path does not appear to be a simple local LAN stream from camera to phone.
- The observed preview-related camera traffic is consistent with cloud-mediated communication or cloud-assisted session/control.
- This does not fully rule out a local service on the camera, because the camera may expose local services that the App simply does not use. P2 port scanning is still required later.

## Comparison Against Earlier Preview Baseline

The structured capture matches the earlier preview baseline:

| Finding | Earlier Preview | Structured Preview |
| --- | --- | --- |
| `ipc79.w390.net` / `120.27.12.196` present | Yes | Yes |
| `devota.av380.net` TLS present | Yes | Yes |
| Direct camera-to-phone flow | Not observed | Not observed |
| Plain HTTP preview request | Not observed | Not observed |
| Large RTP/RTSP-like local video stream | Not observed | Not observed |

## P1-04 Result

P1-04 is complete.

The App preview traffic appears to go through vendor/cloud-related endpoints rather than a direct camera-to-phone LAN video stream.

The strongest observed preview-path candidates are:

```text
ipc79.w390.net / 120.27.12.196
devota.av380.net / 58.221.36.18
```

Next step:

- P1-05: structured PTZ/control capture with explicit action timestamps.
