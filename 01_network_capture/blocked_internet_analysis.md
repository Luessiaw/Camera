# P1-06 Blocked Internet Behavior Analysis

## Scope

This note analyzes the capture taken while the camera stayed connected to the Windows Mobile Hotspot and the PC upstream internet path was interrupted and later restored.

Raw capture:

```text
01_network_capture/pcap_raw/20260514_blocked_internet_camera_192.168.137.177.pcapng
```

Capture metadata:

| Item | Value |
| --- | --- |
| Capture start | 2026-05-14 22:20:30.589533 +08 |
| Duration | 178.127818300 s |
| Packets | 3865 |
| File size | 1666268 bytes |
| Capture filter | `host 192.168.137.177` |
| Camera IP | `192.168.137.177` |
| Phone IP | `192.168.137.29` |
| Hotspot gateway | `192.168.137.1` |

## Test Plan

Planned relative timeline:

| Relative Time | Planned Action |
| ---: | --- |
| 0-20s | Keep camera online as baseline |
| ~20s | Disconnect PC upstream internet while keeping the hotspot active |
| ~60s | Try App preview and one PTZ/control action |
| ~120s | Restore PC upstream internet |
| ~180s | End capture |

Manual App observations are approximate because the actions were recorded by observation rather than a synchronized timer.

## Manual App Observations

| Approx. Relative Time | User Action | App / Device Observation |
| ---: | --- | --- |
| 0s | Stayed in the live preview screen | Preview was already open |
| 40s | Disconnected the router Ethernet cable / upstream internet | Hotspot remained active |
| 50s | Pressed a direction button | Motor moved, but the video image did not update |
| 60s | Exited preview and entered preview again | App reported that it could not connect |
| 120s | Reconnected the router Ethernet cable / upstream internet, then tapped preview | Preview worked normally again |

## High-Level Result

The camera did not become a fully standalone LAN device when public internet was blocked.

The manual observation adds an important nuance: an already-open session could still trigger a PTZ motor movement after upstream internet was disconnected, but video updates stopped and a fresh preview connection failed until upstream internet was restored.

However, the capture gives stronger evidence than previous runs that a local TCP path exists:

```text
63.148773800  192.168.137.177:8800 -> 192.168.137.29:43104  TCP PSH/ACK Len=90
63.148921300  192.168.137.177:8800 -> 192.168.137.29:43104  TCP retransmission Len=90
```

This is local camera-to-phone traffic, not cloud traffic and not a video stream. It should be treated as a candidate local control/session message until repeated captures prove its role.

## Network Timeline

| Relative Time | Evidence | Interpretation |
| ---: | --- | --- |
| 0.000-56.229s | UDP `192.168.137.177 -> 120.27.12.196:8877`; replies still visible early | Existing cloud IPC/keepalive state continued from before the interruption |
| 1.332-121.362s | Repeated ICMP echo from camera to `192.168.137.1` | Local hotspot/gateway path stayed alive |
| 3.810-4.919s | `devota.av380.net` resolved and TLS ClientHello sent to `218.91.199.250:443` | Public internet was still usable near the beginning of the capture |
| ~40s | User disconnected upstream internet | Manual timing; packet evidence shows DNS/cloud failures later in the same test window |
| ~50s | User pressed direction button; motor moved, video did not update | Existing App session could still affect PTZ, but preview media path was not updating |
| ~60s | User exited and re-entered preview; App could not connect | Fresh session setup failed while upstream/cloud path was unavailable |
| 62.815-84.633s | DNS queries for `devota.av380.net`, `ipc79.w390.net`, `ntp.sjtu.edu.cn`, `ntp.av380.net`, and `p2pdispa.av380.net` returned `No such name` | Public DNS/upstream path was failing in the blocked window |
| 63.149s | TCP `192.168.137.177:8800 -> 192.168.137.29:43104`, 90-byte payload, retransmitted | Local camera-to-phone path appeared while cloud name resolution was failing |
| 77.284-82.906s | Repeated TCP SYNs from camera to `120.27.12.196:1340` without responses | Camera kept trying to re-establish cloud IPC while upstream was blocked |
| 84.638-111.965s | TCP SYN attempts to `120.79.255.163:13502`, `47.91.167.51:13502`, `47.254.72.224:13502`, `47.254.133.105:13502` | Camera attempted additional relay/P2P-dispatch style endpoints |
| 115.046-125.831s | UDP 7788/8877 with `120.27.12.196` resumed; UDP `7050 -> 1340` appeared | Cloud IPC recovery began before the large stream |
| ~120s | User restored upstream internet and tapped preview | Manual timing; packet evidence shows cloud/relay recovery immediately afterward |
| 126.364-128.209s | UDP 7050 and TCP 32100 with `121.14.11.152` | Relay/media channel setup candidate |
| 127.541-178.128s | Large TCP 32100 flow with `47.104.64.146`, 3089 packets / 1189 kB | Likely restored video/relay/media traffic |
| 130.018-130.158s | `devota.av380.net` resolved again and TLS ClientHello sent to `218.91.199.250:443` | Public DNS/TLS behavior recovered |
| 173.488s | `ipc79.w390.net` resolved to `120.27.12.196` | Main IPC domain resolution recovered |

## Main Conversations

| Peer | Frames | Bytes | Start | Duration | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `47.104.64.146` | 3089 | 1189 kB | 127.541s | 50.586s | Large TCP 32100 flow after recovery |
| `121.14.11.152` | 389 | 238 kB | 126.364s | 21.846s | UDP 7050 and TCP 32100 setup/media candidate |
| `192.168.137.1` | 95 | 68 kB | 1.332s | 175.162s | Gateway, DNS, ICMP |
| `120.27.12.196` | 61 | 5050 bytes | 0.000s | 177.587s | Existing IPC endpoint, UDP 8877/7788 and TCP 1340 |
| `218.91.199.250` | 58 | 12 kB | 4.866s | 127.333s | `devota.av380.net` TLS |
| `192.168.137.29` | 2 | 312 bytes | 63.149s | 0.000s | Local TCP 8800 camera-to-phone packet and retransmission |

## Local TCP 8800 Payload

The local TCP 8800 packet payload was:

```text
7f2905010000004e000000000500000029000e0036ad94289e010000000000010201d01055c918ead95b60209bc22ad917800000def2314e8f8c2f1fad5c36246114680219ba305926118e3a65cb7f0fdd388213812039e1019c
```

Current interpretation:

| Point | Assessment |
| --- | --- |
| Direction | Camera to phone |
| Protocol | TCP |
| Camera port | 8800 |
| Payload length | 90 bytes |
| Video stream? | No, too small and isolated |
| Local service evidence? | Yes |
| Complete offline control evidence? | Not yet |

## DNS Failure Window

During the blocked window, the hotspot gateway returned DNS `No such name` responses for domains that normally resolve in online captures:

| Relative Time | Domain | Result |
| ---: | --- | --- |
| 62.815s | `devota.av380.net` | A query returned `No such name` |
| 62.830s | `devota.av380.net` | AAAA query returned `No such name` |
| 77.262s | `ipc79.w390.net` | A query returned `No such name` |
| 80.203s | `ntp.sjtu.edu.cn` | A query returned `No such name` |
| 81.261s | `ntp.av380.net` | A query returned `No such name` |
| 84.566s | `p2pdispa.av380.net` | A query returned `No such name` |

This indicates the failure seen by the camera was not only application-level. Name resolution and TCP reachability to cloud endpoints were also disrupted.

## Conclusions

1. The camera remains active on the local hotspot when public internet is blocked.
2. The camera continues probing the hotspot gateway with ICMP while cloud access is failing.
3. Cloud dependency remains strong: the camera repeatedly tries to resolve vendor domains and reconnect to cloud IPC/relay endpoints.
4. A local TCP 8800 path exists and appears again in this scenario, this time from camera to phone.
5. The manual observation suggests PTZ/control can remain briefly usable inside an already-open session after upstream internet is removed.
6. Preview/media does not appear to work fully offline: the image stopped updating, and re-entering preview failed while upstream internet was unavailable.
7. Recovery after internet restoration is visible through DNS success, TLS to `devota.av380.net`, UDP 8877 to `120.27.12.196`, and large TCP 32100 flows to relay/media-like endpoints.

## Updated Hypothesis

The App/camera system likely uses a hybrid design:

- Cloud service discovery and session coordination are required for normal operation.
- `ipc79.w390.net` / `120.27.12.196` remains the core IPC endpoint.
- Local TCP 8800 is present and may carry LAN-side session/control messages or session maintenance messages.
- Existing PTZ/control state may survive briefly after internet loss.
- Fresh preview/media setup appears to depend on cloud/relay behavior unless future tests isolate a direct LAN video path.

## Next Recommended Checks

1. Repeat a shorter blocked-internet test with only one PTZ action at a known timestamp.
2. Repeat a blocked-internet test where preview is closed before disconnecting upstream internet, then reopened after disconnect.
3. In the next local-service phase, scan the camera LAN ports while it is online and while upstream internet is blocked, with special attention to TCP 8800.
4. Try phone-side capture if possible, because camera-filtered capture cannot show phone-to-cloud traffic.
