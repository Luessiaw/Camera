# DNS Analysis

Stage: P1-02

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
| DNS server observed | 192.168.137.1 |

## Result Summary

The camera resolves vendor/cloud domains under two main domain groups:

| Domain Group | Role |
| --- | --- |
| `av380.net` | Main vendor service domain family |
| `w390.net` | Camera cloud channel / IPC communication domain |

The camera also uses `ntp.sjtu.edu.cn` for time synchronization.

No local-domain discovery name, ONVIF service discovery domain, or LAN-only video endpoint domain was observed in these DNS captures.

## Primary DNS Records

| Domain | A Record(s) Observed | Seen In | Initial Role |
| --- | --- | --- | --- |
| `ntp.sjtu.edu.cn` | `17.253.116.253`, `17.253.114.43`, `17.253.114.35` | boot, preview, PTZ | Time sync |
| `svc.av380.net` | `120.24.173.70` | boot | Service region / belonging lookup |
| `alivetype.av380.net` | `8.134.147.2` | boot | Device alive/type registration |
| `alarmserverlist.av380.net` | `219.135.97.79` | boot | Alarm server list lookup |
| `devota.av380.net` | `218.91.199.250`, `58.221.36.18`, `58.221.37.119`, `218.91.170.134` | boot, preview | TLS service endpoint |
| `logs.av380.net` | `39.105.177.250` | boot | Device metadata/log reporting |
| `ipc79.w390.net` | `120.27.12.196` | boot, preview, PTZ | Persistent/custom IPC cloud communication |
| `regipc4379.av380.net` | `47.99.1.63` | boot | Registration-related IPC endpoint |
| `push2.av380.net` | `118.178.56.123` | boot | Detection/alarm push endpoint |

AAAA queries were observed for several `av380.net` domains, but the responses did not return IPv6 addresses in this capture set.

## Domain Details

### `ntp.sjtu.edu.cn`

Observed use:

- The camera resolves `ntp.sjtu.edu.cn`.
- The DNS answer is a CNAME chain ending in Apple CDN time service addresses.
- The camera sends NTP traffic to `17.253.116.253:123`.

Interpretation:

- This is time synchronization.
- It is not a vendor-specific control endpoint.

### `svc.av380.net`

Observed DNS:

```text
svc.av380.net -> 120.24.173.70
```

Observed HTTP:

```text
POST /url/belong
```

Ports:

```text
TCP 8002
```

Interpretation:

- Likely service-region or service-routing lookup.
- This appears early during boot and repeats later in the boot capture.

### `alivetype.av380.net`

Observed DNS:

```text
alivetype.av380.net -> 8.134.147.2
```

Observed HTTP:

```text
POST /v1/ipc/alivetype
```

Ports:

```text
TCP 80
```

Interpretation:

- Likely device alive/type registration.
- One early request returned an "invalid timestamp" style response, then a later request succeeded after time sync.

### `alarmserverlist.av380.net`

Observed DNS:

```text
alarmserverlist.av380.net -> 219.135.97.79
```

Observed HTTP:

```text
POST /api/v3/alarm_server_list
```

Ports:

```text
TCP 8888
```

Interpretation:

- The camera requests alarm/push server list information.
- The HTTP response contains additional push-related names such as `push1.av380.net`, `push2.av380.net`, `pushv.av380.net`, and `nvai*.av380.net`.

### `devota.av380.net`

Observed DNS:

```text
devota.av380.net -> 218.91.199.250, 58.221.36.18, 58.221.37.119, 218.91.170.134
```

Observed TLS:

```text
TLSv1.2 Client Hello
SNI: devota.av380.net
```

Ports:

```text
TCP 443
```

Seen in:

- boot capture
- App preview capture

Interpretation:

- Important encrypted vendor service endpoint.
- Likely device OTA/config/control or secure vendor service channel; exact payload is encrypted.

### `logs.av380.net`

Observed DNS:

```text
logs.av380.net -> 39.105.177.250
```

Observed HTTP:

```text
POST /api/v1/dev/meta
```

Ports:

```text
TCP 9191
```

Interpretation:

- Device metadata or log reporting endpoint.

### `ipc79.w390.net`

Observed DNS:

```text
ipc79.w390.net -> 120.27.12.196
```

Observed traffic:

```text
TCP 1340
UDP 8877
UDP 9001
UDP 7788
UDP 1341
```

Seen in:

- boot capture
- App preview capture
- App PTZ capture

Interpretation:

- This is one of the most important endpoints observed so far.
- The repeated UDP traffic suggests persistent cloud communication, keepalive, relay, registration, or control-channel behavior.
- Because it appears in preview and PTZ captures, it should be prioritized in P1-03.

### `regipc4379.av380.net`

Observed DNS:

```text
regipc4379.av380.net -> 47.99.1.63
```

Observed use:

- Resolved during boot.
- No high-volume conversation was identified in the initial P1-01 conversation summary.

Interpretation:

- Likely registration-related IPC endpoint.
- Needs confirmation in P1-03 if packets to `47.99.1.63` appear in other captures or longer captures.

### `push2.av380.net`

Observed DNS:

```text
push2.av380.net -> 118.178.56.123
```

Observed HTTP:

```text
POST /api/v1/detection/alarm
```

Ports:

```text
TCP 8881
```

Interpretation:

- Detection/alarm push endpoint.
- It is relevant to the user's goal of motion detection and event handling.

## Scenario Comparison

| Scenario | Domains Observed |
| --- | --- |
| Boot online | `ntp.sjtu.edu.cn`, `svc.av380.net`, `alivetype.av380.net`, `alarmserverlist.av380.net`, `devota.av380.net`, `logs.av380.net`, `ipc79.w390.net`, `regipc4379.av380.net`, `push2.av380.net` |
| App preview | `ipc79.w390.net`, `ntp.sjtu.edu.cn`, `devota.av380.net` |
| App PTZ/control | `ntp.sjtu.edu.cn`, `ipc79.w390.net` |

## Initial Priority Ranking

| Priority | Domain | Reason |
| ---: | --- | --- |
| 1 | `ipc79.w390.net` | Appears across boot, preview, and PTZ; has repeated custom UDP/TCP traffic |
| 2 | `devota.av380.net` | Encrypted TLS endpoint, appears in boot and preview |
| 3 | `svc.av380.net` | Service routing / belonging lookup |
| 4 | `alivetype.av380.net` | Device alive/type registration |
| 5 | `alarmserverlist.av380.net` | Returns push/alarm server information |
| 6 | `push2.av380.net` | Detection/alarm reporting |
| 7 | `logs.av380.net` | Metadata/log endpoint |
| 8 | `regipc4379.av380.net` | Registration endpoint candidate, not yet confirmed as active high-volume flow |
| 9 | `ntp.sjtu.edu.cn` | Time sync only |

## P1-02 Result

P1-02 is complete. The primary cloud domains are identified and grouped by observed role.

The next step is P1-03: analyze TCP and UDP communication flows, especially:

- `120.27.12.196` / `ipc79.w390.net`
- `devota.av380.net` over TLS 443
- HTTP service discovery and reporting endpoints under `av380.net`
