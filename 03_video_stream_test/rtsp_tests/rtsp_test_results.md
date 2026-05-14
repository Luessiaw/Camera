# P2-02 RTSP Test Results

Stage: P2-02

Date: 2026-05-14

## Goal

Test whether the camera exposes a common local RTSP stream.

Camera:

| Item | Value |
| --- | --- |
| IP | `192.168.137.177` |
| MAC | `58:c5:87:9a:ab:97` |
| Network | Windows Mobile Hotspot `192.168.137.0/24` |

## Tool Availability

| Tool | Status |
| --- | --- |
| `ffprobe` | Not found in PATH |
| `ffmpeg` | Not found in PATH |
| `curl.exe` | Available, but RTSP protocol is disabled in this Windows build |
| `nmap` | Available |

Because `ffprobe` and `ffmpeg` were unavailable, P2-02 used connection-level checks and manual RTSP request probes. This is sufficient to decide whether common RTSP ports are exposed.

## RTSP / Video Port Check

Raw output:

```text
03_video_stream_test/rtsp_tests/20260514_p2_02_rtsp_ports.txt
03_video_stream_test/rtsp_tests/20260514_p2_02_rtsp_ports.xml
```

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p 554,8554,10554,1554,8555,7070,1935,8000,8080,8800,9800 -oN '03_video_stream_test\rtsp_tests\20260514_p2_02_rtsp_ports.txt' -oX '03_video_stream_test\rtsp_tests\20260514_p2_02_rtsp_ports.xml' 192.168.137.177
```

Result:

| Port | State | Notes |
| ---: | --- | --- |
| 554/tcp | closed | Standard RTSP closed |
| 8554/tcp | closed | Common alternate RTSP closed |
| 10554/tcp | closed | Alternate RTSP closed |
| 1554/tcp | closed | Alternate RTSP-like port closed |
| 1935/tcp | closed | RTMP closed |
| 7070/tcp | closed | RealServer-style streaming port closed |
| 8000/tcp | closed | Common HTTP/video alternate closed |
| 8080/tcp | closed | Common HTTP/video alternate closed |
| 8800/tcp | open | Private camera service candidate |
| 9800/tcp | open | Unknown private service candidate |

## Common RTSP URL Set

The following common URL patterns were considered:

```text
rtsp://192.168.137.177:554/
rtsp://192.168.137.177:554/live
rtsp://192.168.137.177:554/live/ch00_0
rtsp://192.168.137.177:554/live/ch01_0
rtsp://192.168.137.177:554/stream1
rtsp://192.168.137.177:554/11
rtsp://192.168.137.177:8554/
rtsp://192.168.137.177:8554/live
rtsp://192.168.137.177:10554/
```

These URL patterns cannot succeed while their TCP ports are closed or unreachable.

## Manual RTSP Probe

Since `curl.exe` reported:

```text
Protocol "rtsp" disabled
```

manual TCP probes were used to send RTSP `OPTIONS` and `DESCRIBE` requests.

Summary:

| URL | OPTIONS Result | DESCRIBE Result |
| --- | --- | --- |
| `rtsp://192.168.137.177:554/` | connect timeout / unavailable | not tested after unavailable |
| `rtsp://192.168.137.177:8554/` | connect timeout / unavailable | not tested after unavailable |
| `rtsp://192.168.137.177:8800/` | no response | no response |
| `rtsp://192.168.137.177:9800/` | no response | no response |

Interpretation:

- `8800/tcp` and `9800/tcp` accept TCP connections, but they do not respond like RTSP services.
- No SDP response was received.
- There is no evidence that either port is a normal RTSP stream endpoint.

## P2-02 Result

P2-02 is complete.

Current conclusion:

1. No common RTSP port is open.
2. Common RTSP URL patterns on `554/tcp`, `8554/tcp`, and `10554/tcp` are not viable.
3. `8800/tcp` and `9800/tcp` do not respond to basic RTSP `OPTIONS` or `DESCRIBE`.
4. No local RTSP stream was found.

## Next Step Recommendation

Proceed to P2-03 ONVIF testing for completeness, but expected success is low because P1-07 and P2-01 already found `3702/udp` closed.

After P2-03, P2-04 should focus on:

- HTTP/MJPEG checks on common paths and discovered ports.
- Proprietary binary-service checks for `8800/tcp` and `9800/tcp`.
- Capturing traffic while the App opens preview, then correlating local `8800/9800` activity with cloud relay traffic.
