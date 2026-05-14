# Stream Test Results

## RTSP Test

P2-02 result: no local RTSP stream found.

| Target | Tool / Method | Result | Notes |
| --- | --- | --- | --- |
| `rtsp://192.168.137.177:554/*` | nmap port check | Not viable | `554/tcp` is closed |
| `rtsp://192.168.137.177:8554/*` | nmap port check | Not viable | `8554/tcp` is closed |
| `rtsp://192.168.137.177:10554/*` | nmap port check | Not viable | `10554/tcp` is closed |
| `rtsp://192.168.137.177:8800/` | Manual RTSP OPTIONS/DESCRIBE | No RTSP response | TCP port open, but not RTSP-like |
| `rtsp://192.168.137.177:9800/` | Manual RTSP OPTIONS/DESCRIBE | No RTSP response | TCP port open, but not RTSP-like |

Detailed result:

```text
03_video_stream_test/rtsp_tests/rtsp_test_results.md
```

## ONVIF Test

| Tool | Result | Notes |
| --- | --- | --- |
| nmap UDP/TCP ONVIF related ports | No ONVIF service found | `3702/udp` and common ONVIF HTTP ports are closed |
| Manual WS-Discovery Probe | No response | Probe sent to `239.255.255.250:3702` and `192.168.137.177:3702` |

Detailed result:

```text
03_video_stream_test/onvif_tests/onvif_test_results.md
```

## HTTP Stream Test

| URL | Result | Notes |
| --- | --- | --- |
| `http://192.168.137.177/` | No stream found | `80/tcp` is not usable as a web service |
| `http://192.168.137.177:8800/` | No HTTP/MJPEG stream found | TCP connects, but common paths return empty reply |
| `http://192.168.137.177:9800/` | No HTTP/MJPEG stream found | TCP connects, but common paths return empty reply or timeout |

Detailed result:

```text
03_video_stream_test/http_stream_tests/http_mjpeg_private_service_results.md
```

## Private Local Service Test

| Target | Result | Notes |
| --- | --- | --- |
| `192.168.137.177:8800/tcp` | Active during App interaction | Two 16-byte phone-to-camera binary payloads observed |
| `192.168.137.177:9800/tcp` | No App traffic observed | Open port, but not used in the P2-04 dynamic capture |

## Current Stream Decision

No standard local RTSP, ONVIF, HTTP/MJPEG, or obvious local video stream has been found.

Detailed decision:

```text
03_video_stream_test/p2_06_no_flash_stream_decision.md
```

P2-05 is blocked because no usable stream is available for codec/resolution/frame-rate measurement.

Recommended next phase: P3 read-only UART investigation.
