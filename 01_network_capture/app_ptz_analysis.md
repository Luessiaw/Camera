# App PTZ Control Traffic Analysis

Stage: P1-05

Source captures:

```text
01_network_capture/pcap_raw/20260514_app_ptz_camera_192.168.137.177.pcapng
01_network_capture/pcap_raw/20260514_app_ptz_structured_camera_192.168.137.177.pcapng
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
| `20260514_app_ptz_camera_192.168.137.177.pcapng` | 60s | 79 | 31256 bytes | Initial App PTZ/control baseline |
| `20260514_app_ptz_structured_camera_192.168.137.177.pcapng` | 120s | 122 | 56704 bytes | Structured PTZ capture with planned directional actions |

## Manual Action Log

| Relative Time | Action | Result |
| ---: | --- | --- |
| 12s | Up | Success |
| 21s | Down | Success |
| 31-38s | Left | App stalled and showed "connecting"; motor moved after the stall |
| 40s | Right | Success |
| 50s | Left | Success |
| 60s | Right | Success |

Observed stall:

| Item | Value |
| --- | --- |
| Stall start | About 31s |
| Recovery | About 38s |
| Video interruption | Yes |
| Actual PTZ movement | Yes |
| Other abnormal behavior | None |

## Structured PTZ Capture Findings

Main IPv4 conversations:

| Remote | Packets | Bytes | Notes |
| --- | ---: | ---: | --- |
| `192.168.137.1` | 56 | about 47 kB | Gateway, DNS, DHCP, and local ICMP/ping-related traffic |
| `120.27.12.196` | 49 | 3658 bytes | `ipc79.w390.net`, TCP 1340 and UDP custom traffic |
| `17.253.116.125` | 3 | 270 bytes | NTP |
| `192.168.137.29` | 2 | 164 bytes | Phone-to-camera TCP 8800 payload |
| `120.25.210.108` | 2 | 180 bytes | `ntp.av380.net` NTP |

## Local Phone-to-Camera Observation

The structured PTZ capture contains a local phone-to-camera packet that was not prominent in the preview analysis.

Observed flow:

| Relative Time | Source | Destination | Protocol | Payload |
| ---: | --- | --- | --- | --- |
| 26.439911s | `192.168.137.29:39202` | `192.168.137.177:8800` | TCP | 16 bytes |
| 26.440066s | `192.168.137.29:39202` | `192.168.137.177:8800` | TCP retransmission | same 16 bytes |

Payload hex:

```text
bc000000000000000000000000000000
```

Interpretation:

- This suggests the App may send at least some local LAN command, heartbeat, or control signal to the camera on TCP port 8800.
- Because the packet is only 16 bytes and appears once with a retransmission, it is not a video stream.
- The packet appears after the successful down action at 21s and before the left action/stall beginning around 31s.
- It may be related to PTZ state, but this single observation is not enough to map the payload to a specific direction.

## Cloud Flow Around Local PTZ Signal

Near the local `TCP 8800` packet, the camera refreshes or re-establishes cloud communication with `120.27.12.196`:

| Relative Time | Event |
| ---: | --- |
| 26.440s | Phone sends 16-byte TCP payload to camera `8800` |
| 28.786s | Camera queries DNS for `ipc79.w390.net` |
| 28.805s | DNS response maps `ipc79.w390.net` to `120.27.12.196` |
| 28.814s | Camera opens TCP `120.27.12.196:1340` |
| 28.839s | Camera immediately closes TCP `1340` |
| 28.839s | Camera sends UDP `120.27.12.196:1341` |
| 28.856s | Camera sends UDP `120.27.12.196:9001` |
| 28.877s | Camera receives UDP `9001` response |
| 30.220s | Camera sends UDP `120.27.12.196:7788` |
| 30.395s | Camera receives UDP `7788` response |
| 30.398s | Camera starts UDP `120.27.12.196:8877` recurring flow |

Manual correlation:

- The local `TCP 8800` packet appears at 26.44s.
- The cloud IPC refresh begins at about 28.79s.
- The left action caused the App to show "connecting" at about 31s and recover at about 38s.
- This places the cloud IPC refresh immediately before the visible App stall.
- During the stall window, UDP `8877` request/response traffic continues at 30.398s/30.417s, 32.989s/33.008s, and 35.590s/35.609s.

Interpretation:

- The camera-side cloud channel did not fully stop during the visible App stall.
- The stall may be caused by phone/App-to-cloud instability, video-session renegotiation, or cloud relay/control state changes rather than a complete camera network outage.
- The eventual motor movement after the stall suggests the PTZ command was delayed, queued, or retried rather than dropped.

## `ipc79.w390.net` / `120.27.12.196` PTZ Pattern

Observed ports:

| Protocol | Port | Pattern |
| --- | ---: | --- |
| TCP | 1340 | Short handshake and close, seen around 28.8s and again around 112.0s |
| UDP | 1341 | Short outbound packet near TCP 1340 setup |
| UDP | 9001 | Short request/response |
| UDP | 7788 | 64-byte outbound packet and 16-byte response |
| UDP | 8877 | Repeated packets over most of the capture |

The later sequence around 112s repeats the same setup pattern:

| Relative Time | Event |
| ---: | --- |
| 111.994s | Camera queries `ipc79.w390.net` |
| 111.998s | Camera opens TCP `120.27.12.196:1340` |
| 112.028s | UDP `1341` |
| 112.045s | UDP `9001` |
| 113.427s | UDP `7788` |
| 113.481s | UDP `8877` |

Interpretation:

- PTZ/control behavior involves the same cloud IPC endpoint as preview.
- The local TCP 8800 packet suggests a possible hybrid path: App sends a small local signal while the camera maintains or refreshes cloud IPC state.
- Alternatively, the local packet may be unrelated local heartbeat/control, and PTZ may still be primarily cloud mediated.

## App Connecting Consideration

The user reported that pressing direction keys sometimes makes the App stall and display "connecting".

Evidence to consider:

- The visible stall happened near 31s and recovered near 38s.
- This correlates with the `TCP 8800` packet at 26.44s and the `ipc79.w390.net` re-setup beginning around 28.79s.
- UDP `8877` continued during the stall window, so the camera-side cloud channel was not completely silent.
- This capture was filtered around the camera, not the phone's cloud traffic.
- If the phone-to-cloud path stalls while camera-to-cloud remains healthy, this camera-side capture can only infer it indirectly.

## P1-05 Result

P1-05 is complete.

The structured PTZ/control traffic identified three important findings:

1. A local phone-to-camera TCP `8800` packet with 16-byte payload appears during the PTZ capture.
2. The camera still uses `ipc79.w390.net` / `120.27.12.196` custom TCP/UDP cloud traffic during the control window.
3. The visible App stall around 31-38s correlates with cloud IPC refresh/re-setup timing, but camera-side UDP `8877` traffic continues during the stall.

Current interpretation:

- PTZ control may use a hybrid path: a small local phone-to-camera signal plus cloud IPC/control state through `ipc79.w390.net`.
- The App stall is likely not caused by a total camera network outage, because camera-to-cloud UDP traffic continues.
- The stall may be in the App/video/control session layer, the phone-to-cloud path, or a cloud relay/control state transition.
- More repeated direction-specific captures would be needed to map `TCP 8800` payloads to exact PTZ directions.

Next step:

- P1-06: block public internet and observe whether the camera still exposes any local service or responds to App/local control.
