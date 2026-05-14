# P2-06 Local Stream Decision

Stage: P2-06

Date: 2026-05-14

## Goal

Decide whether the camera can be used without firmware or serial work by directly pulling a local video stream from the LAN.

## Decision

Current decision:

```text
No. A usable local video stream has not been found.
```

P2-05 is therefore blocked because there is no stream whose codec, resolution, frame rate, or bitrate can be measured.

The project should not proceed directly to server-side video ingestion through P6-04 yet.

## Evidence Summary

| Stage | Evidence | Result |
| --- | --- | --- |
| P1-04 | App preview capture | No direct camera-to-phone LAN video stream observed |
| P1-06 | Blocked internet test | Existing session could move PTZ, but video stopped updating and fresh preview failed |
| P1-07 | Local video interface assessment | No standard RTSP / HTTP-MJPEG / ONVIF interface found; `8800/tcp` open |
| P2-01 | Full TCP and UDP port scan | Stable candidates are `8800/tcp` and `9800/tcp`; no standard video service found |
| P2-02 | RTSP testing | No local RTSP stream found |
| P2-03 | ONVIF testing | No ONVIF / WS-Discovery interface found |
| P2-04 | HTTP/MJPEG and private service checks | No HTTP/MJPEG stream found; `8800/tcp` carries small binary payloads, not video |

## Protocol-Level Findings

### Standard Local Protocols

| Protocol / Interface | Current Status |
| --- | --- |
| RTSP | Not found; `554/tcp`, `8554/tcp`, and `10554/tcp` are closed |
| ONVIF | Not found; `3702/udp` closed and WS-Discovery probe received no response |
| HTTP/MJPEG | Not found; common paths on `80/tcp`, `8800/tcp`, and `9800/tcp` did not return usable HTTP/MJPEG |
| SSDP / mDNS | Not found in UDP scans |

### Private Local Services

| Service | Current Status |
| --- | --- |
| `8800/tcp` | Open, active during App interaction, carries small binary phone-to-camera payloads |
| `9800/tcp` | Open, unknown, no App traffic observed in P2-04 dynamic capture |

Observed `8800/tcp` payload examples:

```text
bc000000000000000000000000000000
aa000000e803e803ea03e80300000000
```

These payloads are too small to be video. They are better treated as control, heartbeat, session, or proprietary signaling candidates.

## Cloud Dependency Assessment

The App preview path still appears cloud-dependent:

- The camera repeatedly uses `devota.av380.net` over TLS.
- The camera repeatedly uses `ipc79.w390.net` / `120.27.12.196` over TCP 1340 and UDP 1341/9001/7788/8877.
- When public internet was blocked, video stopped updating and fresh preview could not reconnect.
- Dynamic local-service capture during App operation did not show a local high-volume media flow.

## Practical Conclusion

The current evidence does not support a no-flash, no-serial path based on standard local stream pulling.

Possible paths from here:

| Path | Recommendation | Reason |
| --- | --- | --- |
| Continue P2 standard stream testing | Low value | RTSP, ONVIF, HTTP/MJPEG have already failed |
| Reverse `8800/tcp` / `9800/tcp` from traffic only | Possible but not first choice | Protocol is private; current payloads look like signaling, not media |
| Cloud protocol emulation | Possible but high complexity | TLS, tokens, relay coordination, and private UDP/TCP behavior likely need deeper reverse engineering |
| P3 read-only UART | Recommended next | Low write-risk and likely to expose boot logs, process names, service names, and port ownership |
| Firmware modification | Not recommended yet | Requires UART evidence and P4 full flash backup first |

## Recommended Next Step

Proceed to P3 with a read-only UART investigation.

Safety boundary for P3:

1. Do not write firmware.
2. Do not connect USB-TTL TX to camera RX initially.
3. First identify GND and voltage levels.
4. Confirm UART is 3.3 V TTL before connecting.
5. Capture boot logs with camera TX -> USB-TTL RX only.

The most useful P3 evidence will be:

- Kernel boot log
- Root filesystem hints
- Init scripts
- Process names
- Network service startup logs
- Which process owns `8800/tcp` and `9800/tcp`
- Whether hidden RTSP/media components exist but are disabled

## P2-06 Result

P2-06 is complete.

Decision:

```text
Do not proceed as if local stream接管 is available.
Move to P3 read-only UART before any firmware backup or modification work.
```
