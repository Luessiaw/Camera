# P2-04 HTTP/MJPEG and Private Service Results

Stage: P2-04

Date: 2026-05-14

## Goal

Test whether the camera exposes a local HTTP/MJPEG stream or whether the discovered private ports `8800/tcp` and `9800/tcp` show evidence of local video transport.

Camera:

| Item | Value |
| --- | --- |
| IP | `192.168.137.177` |
| MAC | `58:c5:87:9a:ab:97` |
| Phone IP | `192.168.137.29` |
| Network | Windows Mobile Hotspot `192.168.137.0/24` |

## Static HTTP/MJPEG Probe

Ports checked:

```text
80/tcp
8800/tcp
9800/tcp
```

Paths checked:

```text
/
/video
/video.cgi
/videostream.cgi
/mjpeg
/mjpeg.cgi
/snapshot.jpg
/snap.jpg
/image.jpg
/stream
/live
/cgi-bin/snapshot.cgi
/webcapture.jpg
```

Results:

| Port | Result |
| ---: | --- |
| 80/tcp | No usable HTTP response; port was not reachable as a web service |
| 8800/tcp | TCP connection accepted, but all tested HTTP/MJPEG paths returned empty reply |
| 9800/tcp | TCP connection accepted, but tested HTTP/MJPEG paths returned empty reply or timeout |

Interpretation:

- No HTTP status line, content type, JPEG response, multipart MJPEG stream, or usable web page was observed.
- `8800/tcp` and `9800/tcp` are not normal HTTP/MJPEG endpoints.

## Dynamic App Capture

Capture file:

```text
03_video_stream_test/http_stream_tests/20260514_p2_04_app_preview_private_ports_camera_192.168.137.177.pcapng
```

Capture metadata:

| Item | Value |
| --- | --- |
| Capture start | 2026-05-14 23:00:45.628478600 +08 |
| Duration | 95.776676100 s |
| Packets | 153 |
| File size | 61 kB |
| Capture filter | `host 192.168.137.177` |

Planned manual actions:

| Relative Time | Planned Action |
| ---: | --- |
| 0s | Keep App outside preview |
| 10s | Enter preview |
| 25s | Keep preview stable |
| 40s | Press one direction key |
| 55s | Exit preview |
| 70s | Enter preview again |
| 90s | Stop interacting |

## Dynamic Capture Conversations

IPv4 conversation summary:

| Peer | Frames | Bytes | Start | Duration | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `218.91.170.134` | 57 | 12 kB | 9.316s | 61.561s | TLS with SNI `devota.av380.net` |
| `192.168.137.1` | 50 | 40 kB | 0.000s | 95.777s | Gateway, DNS, DHCP |
| `120.27.12.196` | 31 | 2274 bytes | 8.550s | 86.685s | `ipc79.w390.net` cloud IPC endpoint |
| `192.168.137.29` | 4 | 328 bytes | 38.603s | 3.267s | Local phone-to-camera TCP 8800 packets |
| `17.253.116.253` | 2 | 180 bytes | 44.281s | 0.073s | NTP |

TCP conversation summary:

| Flow | Frames | Bytes | Notes |
| --- | ---: | ---: | --- |
| `192.168.137.177:* -> 218.91.170.134:443` | 57 | 12 kB | Two short TLS sessions |
| `192.168.137.177:* -> 120.27.12.196:1340` | 9 | 610 bytes | Short cloud IPC setup |
| `192.168.137.29:* -> 192.168.137.177:8800` | 4 | 328 bytes | Two 16-byte local payloads, each retransmitted |

UDP conversation summary:

| Flow | Frames | Bytes | Notes |
| --- | ---: | ---: | --- |
| `192.168.137.177:* -> 120.27.12.196:8877` | 17 | 1326 bytes | Repeated small cloud IPC packets |
| `192.168.137.177:* -> 120.27.12.196:9001` | 2 | 116 bytes | Short cloud IPC exchange |
| `192.168.137.177:* -> 120.27.12.196:7788` | 2 | 164 bytes | Short cloud IPC exchange |
| `192.168.137.177:* -> 120.27.12.196:1341` | 1 | 58 bytes | Short cloud IPC packet |

## Local TCP 8800 Payloads

Two local phone-to-camera payloads were observed:

| Relative Time | Source | Destination | Payload Length | Payload |
| ---: | --- | --- | ---: | --- |
| 38.602728500s | `192.168.137.29:56854` | `192.168.137.177:8800` | 16 bytes | `aa000000e803e803ea03e80300000000` |
| 41.869496000s | `192.168.137.29:56858` | `192.168.137.177:8800` | 16 bytes | `bc000000000000000000000000000000` |

Each packet was retransmitted once.

Interpretation:

- `8800/tcp` is active during App interaction.
- The payloads are small and binary.
- This looks more like local control/session signaling than video transport.
- The second payload `bc000000000000000000000000000000` matches the earlier P1-05 local TCP 8800 observation.
- The first payload beginning with `aa000000...` is new evidence and may be related to the direction-key action or local session state.

## TCP 9800 Observation

No `9800/tcp` traffic appeared in the dynamic App capture.

Interpretation:

- `9800/tcp` is open, but it was not used by the App during this preview/control scenario.
- It remains an unknown private service candidate, but there is no current evidence that it carries preview video.

## Cloud Path Observation

During the same capture, the camera still used:

| Endpoint | Evidence |
| --- | --- |
| `devota.av380.net` / `218.91.170.134:443` | DNS resolution and TLS ClientHello at about 9.36s and 68.40s |
| `ipc79.w390.net` / `120.27.12.196` | DNS resolution at about 44.24s, TCP 1340, UDP 1341/9001/7788/8877 |

No local high-volume video-like flow was found. The total capture was only 153 packets / 61 kB over about 96 seconds, which is far too small for a local video stream.

## P2-04 Result

P2-04 is complete.

Current conclusion:

1. No local HTTP/MJPEG stream was found.
2. `8800/tcp` is a real local private camera service used during App interaction.
3. `8800/tcp` carries small binary payloads, not a visible video stream.
4. `9800/tcp` is open but was not used in this App preview/control capture.
5. App preview/control still correlates with cloud endpoints, especially `devota.av380.net` and `ipc79.w390.net`.
6. There is still no evidence of a standard local video interface.

## Next Step Recommendation

Proceed to P2-05 only if a usable video stream exists. Based on P2-02, P2-03, and P2-04, no such stream has been found, so P2-05 is currently blocked.

Recommended next task:

- Run P2-06 as a decision gate: determine whether the project can proceed without firmware/serial work.

Likely decision:

- Standard local video接管 is not currently available.
- Continue toward P3 read-only UART investigation before any firmware modification.
- Keep `8800/tcp` and `9800/tcp` as later proprietary protocol analysis targets, especially after UART/firmware evidence identifies the running services.
