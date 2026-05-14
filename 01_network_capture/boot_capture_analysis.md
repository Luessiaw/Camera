# Boot Capture Analysis

Stage: P1-01

Capture file:

```text
01_network_capture/pcap_raw/20260514_2104_boot_online_camera_192.168.137.177.pcapng
```

Capture metadata:

| Item | Value |
| --- | --- |
| Scenario | Camera boot with internet access |
| Duration | 120s |
| Packet count | 288 |
| Capture filter | `host 192.168.137.177` |
| Camera IP | 192.168.137.177 |
| Camera MAC | 58:c5:87:9a:ab:97 |
| Hotspot gateway | 192.168.137.1 |
| Capture interface | Windows Mobile Hotspot / `本地连接* 10` |

## Protocol Summary

| Protocol | Frames | Notes |
| --- | ---: | --- |
| IP | 283 | Most packets are IPv4 |
| TCP | 182 | HTTP, TLS, and cloud service connections |
| UDP | 71 | DNS, DHCP, NTP, and custom UDP traffic |
| DNS | 42 | Cloud domain and NTP resolution |
| DHCP | 2 | DHCP Offer and ACK from 192.168.137.1 |
| NTP | 2 | Time sync with `ntp.sjtu.edu.cn` resolved to Apple CDN addresses |
| HTTP | 16 | Plain HTTP JSON service calls |
| TLS | 22 | TLSv1.2 traffic with SNI `devota.av380.net` |
| ICMP | 15 | Ping traffic from earlier reachability checks |
| ARP | 5 | Local link discovery |

## Boot-Stage Timeline

Times are relative to the pcap start, not absolute wall-clock time.

| Relative Time | Event |
| ---: | --- |
| 0.000s | Existing UDP traffic with `120.27.12.196:8877` is already present at capture start |
| 49.279s | DHCP Offer from `192.168.137.1` to camera |
| 49.319s | DHCP ACK from `192.168.137.1` to camera |
| 49.607s | DNS query for `ntp.sjtu.edu.cn` |
| 49.624s | NTP request to `17.253.116.253:123` |
| 49.668s | DNS queries for `svc.av380.net`, `alivetype.av380.net`, and `alarmserverlist.av380.net` |
| 49.720s | TCP connections start to `8.134.147.2:80`, `219.135.97.79:8888`, and `120.24.173.70:8002` |
| 49.779s | HTTP POST to `alarmserverlist.av380.net:8888/api/v3/alarm_server_list` |
| 49.781s | HTTP POST to `alivetype.av380.net/v1/ipc/alivetype` |
| 49.781s | HTTP POST to `svc.av380.net/url/belong` |
| 50.326s | HTTP GET to `119.23.22.242` using an encoded `param` query |
| 50.658s | DNS query for `devota.av380.net` |
| 51.342s | DNS query for `logs.av380.net` |
| 51.388s | HTTP POST to `logs.av380.net:9191/api/v1/dev/meta` |
| 52.524s | DNS query for `ipc79.w390.net` |
| 52.642s | DNS query for `regipc4379.av380.net` |
| 52.683s | TCP connection to `120.27.12.196:1340` |
| 52.706s | UDP traffic to `120.27.12.196:1341` |
| 52.719s | UDP traffic to `120.27.12.196:9001` |
| 52.837s | TLS Client Hello to `devota.av380.net` via `58.221.37.119:443` |
| 53.644s | UDP traffic to `120.27.12.196:7788` |
| 53.708s | UDP traffic to `120.27.12.196:8877` |
| 59.679s | DNS query for `push2.av380.net` |
| 59.746s | HTTP POST to `push2.av380.net:8881/api/v1/detection/alarm` |
| 61.068s | TLS Client Hello to `devota.av380.net` via `218.91.199.250:443` |
| 110.530s | Repeated DNS query for `svc.av380.net` |
| 110.603s | Repeated HTTP POST to `svc.av380.net/url/belong` |

## Observed Cloud Domains

| Domain | Resolved Address(es) | Observed Use |
| --- | --- | --- |
| `ntp.sjtu.edu.cn` | `17.253.116.253`, `17.253.114.43`, `17.253.114.35` | Time sync |
| `svc.av380.net` | `120.24.173.70` | Service region / belonging lookup over HTTP |
| `alivetype.av380.net` | `8.134.147.2` | IPC alive/type registration over HTTP |
| `alarmserverlist.av380.net` | `219.135.97.79` | Alarm server list lookup over HTTP |
| `devota.av380.net` | `218.91.199.250`, `58.221.36.18`, `58.221.37.119`, `218.91.170.134` | TLS endpoint with SNI `devota.av380.net` |
| `logs.av380.net` | `39.105.177.250` | Device metadata/log reporting over HTTP |
| `ipc79.w390.net` | `120.27.12.196` | Persistent/custom TCP and UDP communication |
| `regipc4379.av380.net` | `47.99.1.63` | Resolved during boot, no direct conversation observed in this capture summary |
| `push2.av380.net` | `118.178.56.123` | Detection/alarm HTTP endpoint |

## Main Remote Connections

| Remote | Port/Protocol | Notes |
| --- | --- | --- |
| `192.168.137.1` | UDP 53 / DHCP / ICMP | DNS, DHCP, gateway, and ping target |
| `120.27.12.196` | UDP 8877, 9001, 7788; TCP 1340 | Persistent/custom camera cloud traffic; maps to `ipc79.w390.net` |
| `120.24.173.70` | TCP 8002 / HTTP | `svc.av380.net` |
| `8.134.147.2` | TCP 80 / HTTP | `alivetype.av380.net` |
| `219.135.97.79` | TCP 8888 / HTTP | `alarmserverlist.av380.net` |
| `39.105.177.250` | TCP 9191 / HTTP | `logs.av380.net` |
| `58.221.37.119` | TCP 443 / TLS | `devota.av380.net` |
| `218.91.199.250` | TCP 443 / TLS | `devota.av380.net` |
| `118.178.56.123` | TCP 8881 / HTTP | `push2.av380.net` |
| `119.23.22.242` | TCP 80 / HTTP | Plain HTTP GET with encoded parameter |

## Initial Interpretation

- The boot-stage capture is valid for P1-01: it contains DHCP, DNS, time sync, HTTP service discovery, TLS setup, and custom UDP traffic.
- The camera strongly depends on vendor/cloud endpoints during boot.
- Several HTTP requests are plaintext and expose service paths, but the detailed payload meaning should be handled in P1-02/P1-03.
- `ipc79.w390.net` / `120.27.12.196` appears important because it is present from the start and later receives repeated UDP keepalive-like traffic.
- The capture does not show a simple local camera-to-phone boot path.

## P1-01 Result

P1-01 is complete. The saved boot capture contains enough data to proceed to:

- P1-02: DNS request analysis.
- P1-03: TCP/UDP communication flow analysis.
