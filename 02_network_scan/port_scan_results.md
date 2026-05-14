# Port Scan Results

Stage: P2-01

Date: 2026-05-14

## Device

| Item | Value |
| --- | --- |
| Camera IP | `192.168.137.177` |
| Camera MAC | `58:c5:87:9a:ab:97` |
| Network | Windows Mobile Hotspot `192.168.137.0/24` |
| Scanner | Windows PC / hotspot gateway |
| Tool | Nmap 7.99 |

## Raw Output Files

Raw nmap outputs are stored under `02_network_scan/nmap/`.

| File | Purpose |
| --- | --- |
| `20260514_p2_01_tcp_all_ports.txt` | Full TCP port scan |
| `20260514_p2_01_tcp_all_ports.xml` | Full TCP port scan XML |
| `20260514_p2_01_udp_top100.txt` | UDP top-100 scan |
| `20260514_p2_01_udp_top100.xml` | UDP top-100 scan XML |
| `20260514_p2_01_open_ports_service.txt` | Deep service fingerprint on discovered ports |
| `20260514_p2_01_open_ports_service.xml` | Deep service fingerprint XML |
| `20260514_p2_01_open_ports_service_light.txt` | Light service fingerprint on discovered ports |
| `20260514_p2_01_open_ports_service_light.xml` | Light service fingerprint XML |
| `20260514_p2_01_tcp_open_ports_rescan.txt` | Quick rescan of discovered TCP ports |
| `20260514_p2_01_tcp_open_ports_rescan.xml` | Quick rescan XML |

## Reachability

The camera responded to ICMP:

```text
Reply from 192.168.137.177: bytes=32 time=2ms TTL=64
Reply from 192.168.137.177: bytes=32 time=14ms TTL=64
```

## Full TCP Scan

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p- --min-rate 1000 -oN '02_network_scan\nmap\20260514_p2_01_tcp_all_ports.txt' -oX '02_network_scan\nmap\20260514_p2_01_tcp_all_ports.xml' 192.168.137.177
```

Result:

```text
Not shown: 65530 closed tcp ports (conn-refused)
PORT     STATE SERVICE     REASON
25/tcp   open  smtp        syn-ack
110/tcp  open  pop3        syn-ack
143/tcp  open  imap        syn-ack
8800/tcp open  sunwebadmin syn-ack
9800/tcp open  davsrc      syn-ack
```

## Open-Port Rescan

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p 25,110,143,8800,9800 -oN '02_network_scan\nmap\20260514_p2_01_tcp_open_ports_rescan.txt' -oX '02_network_scan\nmap\20260514_p2_01_tcp_open_ports_rescan.xml' 192.168.137.177
```

Result:

```text
PORT     STATE SERVICE     REASON
25/tcp   open  smtp        syn-ack
110/tcp  open  pop3        syn-ack
143/tcp  open  imap        syn-ack
8800/tcp open  sunwebadmin syn-ack
9800/tcp open  davsrc      syn-ack
```

## Service Fingerprint

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sV -Pn -n --version-intensity 2 --reason -p 25,110,143,8800,9800 -oN '02_network_scan\nmap\20260514_p2_01_open_ports_service_light.txt' -oX '02_network_scan\nmap\20260514_p2_01_open_ports_service_light.xml' 192.168.137.177
```

Result:

```text
PORT     STATE  SERVICE        REASON         VERSION
25/tcp   closed smtp           reset ttl 64
110/tcp  closed pop3           reset ttl 64
143/tcp  closed imap           reset ttl 64
8800/tcp open   unknown-camera syn-ack ttl 64 V308 camera service
9800/tcp open   davsrc?        syn-ack ttl 64
MAC Address: 58:C5:87:9A:AB:97 (AltoBeam)
Service Info: Device: webcam
```

Interpretation:

- `8800/tcp` is stable and matches the previous P1 evidence.
- `9800/tcp` is also open and should be investigated with `8800/tcp`.
- `25/tcp`, `110/tcp`, and `143/tcp` appear open in plain connect scans, but service fingerprint scans report them closed/reset.
- The port-number labels `smtp`, `pop3`, and `imap` should not be treated as real mail-service evidence. No banner was observed.

## UDP Top-100 Scan

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sU -Pn -n --reason --top-ports 100 -oN '02_network_scan\nmap\20260514_p2_01_udp_top100.txt' -oX '02_network_scan\nmap\20260514_p2_01_udp_top100.xml' 192.168.137.177
```

Result:

```text
All 100 scanned ports on 192.168.137.177 are in ignored states.
Not shown: 100 closed udp ports (port-unreach)
```

Interpretation:

- No common UDP service was found.
- This supports the earlier P1-07 result that ONVIF WS-Discovery, SSDP, and mDNS were not visible.

## Basic Banner / HTTP Checks

Initial banner checks:

| Port | Result |
| ---: | --- |
| 25/tcp | No initial banner |
| 110/tcp | No initial banner |
| 143/tcp | No initial banner |
| 8800/tcp | No initial banner |
| 9800/tcp | No initial banner |

HTTP checks:

| Port | HTTP Probe Result |
| ---: | --- |
| 25/tcp | Connection established, then reset |
| 110/tcp | Connection established, then reset |
| 143/tcp | Connection established, then reset |
| 8800/tcp | Connection established, empty reply |
| 9800/tcp | Connection established, empty reply |

## Summary

| Port | Protocol | State | Stability | Notes |
| ---: | --- | --- | --- | --- |
| 25 | TCP | Open in connect scan, closed/reset during service scan | Unstable / unclear | No banner; do not assume SMTP |
| 110 | TCP | Open in connect scan, closed/reset during service scan | Unstable / unclear | No banner; do not assume POP3 |
| 143 | TCP | Open in connect scan, closed/reset during service scan | Unstable / unclear | No banner; do not assume IMAP |
| 8800 | TCP | Open | Stable | Nmap fingerprint: `unknown-camera` / `V308 camera service`; binary/private service candidate |
| 9800 | TCP | Open | Stable | Unknown service; HTTP returns empty reply |
| Top 100 UDP | UDP | Closed | Stable | No common UDP service found |

## P2-01 Result

P2-01 is complete.

The useful local-service candidates are:

```text
192.168.137.177:8800/tcp
192.168.137.177:9800/tcp
```

No standard RTSP, HTTP, HTTP/MJPEG, ONVIF, SSDP, or mDNS service was found in this scan.

Next recommended task:

- P2-02: test common RTSP URLs, but expected success is low because `554/tcp` and `8554/tcp` are closed.
- P2-04 should later include proprietary checks for `8800/tcp` and `9800/tcp`.
