# P1-07 Local Video Interface Assessment

Stage: P1-07

## Scope

Goal: determine whether the camera exposes a directly usable LAN video interface such as RTSP, HTTP/MJPEG, ONVIF, or another obvious local stream endpoint.

Camera:

| Item | Value |
| --- | --- |
| IP | `192.168.137.177` |
| MAC | `58:c5:87:9a:ab:97` |
| Vendor OUI | AltoBeam |
| Test network | Windows Mobile Hotspot `192.168.137.0/24` |

## Current Task Assessment

No major task-order change is required before P1-07.

Minor adjustment:

- P1-07 should not rely only on packet captures, because P1-05 and P1-06 both exposed local TCP 8800 evidence.
- P1-07 should therefore include an active local-service check for common video ports and TCP 8800.
- P2-01 is still needed later as a fuller port inventory, but P1-07 can already answer whether a common local video interface is obvious.

## Tests Performed

### Reachability

```text
ping.exe -n 2 192.168.137.177
```

Result:

```text
Reply from 192.168.137.177: bytes=32 time=1ms TTL=64
Reply from 192.168.137.177: bytes=32 time=2ms TTL=64
```

The camera was reachable on the hotspot LAN.

### Common TCP Video / Service Ports

Command:

```text
nmap -sT -Pn -n --reason -p 80,81,88,443,554,8554,8000,8080,8081,8090,5000,5001,8899,8800,8999,9000,9001,10000,10554,37777,34567,3702 192.168.137.177
```

Result summary:

| Port | State | Interpretation |
| ---: | --- | --- |
| 80/tcp | closed | No HTTP web interface on default port |
| 443/tcp | closed | No HTTPS web interface on default port |
| 554/tcp | closed | No standard RTSP port |
| 8554/tcp | closed | No common alternate RTSP port |
| 8080/tcp | closed | No common HTTP alternate port |
| 8899/tcp | closed | No common ONVIF/vendor discovery TCP port |
| 8800/tcp | open | Private camera service candidate |
| Other tested TCP ports | closed | No obvious common stream/service endpoint |

### Service Fingerprint

Command:

```text
nmap -sV -Pn -n --version-light --reason -p 8800,80,554,8554,8080,8899 192.168.137.177
```

Result:

```text
80/tcp   closed http
554/tcp  closed rtsp
8080/tcp closed http-proxy
8554/tcp closed rtsp-alt
8800/tcp open   unknown-camera  V308 camera service
8899/tcp closed ospf-lite
```

Nmap identifies `8800/tcp` as a camera-like service, but not as RTSP, HTTP, or ONVIF.

### UDP Discovery Ports

Command:

```text
nmap -sU -Pn -n --reason -p 3702,1900,5000,5353,8899,8800 192.168.137.177
```

Result:

| Port | State | Interpretation |
| ---: | --- | --- |
| 3702/udp | closed | No WS-Discovery / ONVIF response |
| 1900/udp | closed | No SSDP/UPnP response |
| 5353/udp | closed | No mDNS response |
| 8800/udp | closed | TCP 8800 only in this check |
| 8899/udp | closed | No common vendor UDP discovery response |

### HTTP Probe on TCP 8800

Command:

```text
curl.exe -v --connect-timeout 2 http://192.168.137.177:8800/
```

Result:

```text
Connected to 192.168.137.177:8800
GET / HTTP/1.1
Empty reply from server
```

Interpretation:

- TCP 8800 accepts a connection.
- It does not behave like a normal HTTP endpoint.
- This matches the packet captures where TCP 8800 carries short binary payloads.

## Cross-Reference With Packet Captures

P1-05:

```text
192.168.137.29:39202 -> 192.168.137.177:8800
payload: bc000000000000000000000000000000
```

P1-06:

```text
192.168.137.177:8800 -> 192.168.137.29:43104
payload length: 90 bytes
```

These observations support the same conclusion as the active scan: `8800/tcp` is a real local camera service, but it is not an obvious standard video stream.

## Result

P1-07 is complete at the initial local-interface level.

Current conclusion:

1. No directly usable standard RTSP interface was found.
2. No obvious HTTP/MJPEG interface was found.
3. No ONVIF/WS-Discovery response was found.
4. A proprietary local camera service exists on `8800/tcp`.
5. There is no current evidence that `8800/tcp` is a raw video stream.
6. Video preview still appears to depend on cloud/relay behavior based on P1-04 and P1-06.

## Impact on Follow-Up Tasks

The overall task order does not need a large change, but the emphasis should change:

- P2-01 should still perform a fuller port scan to make sure no uncommon port was missed.
- P2-02 can still test common RTSP URLs, but the probability of success is now low because `554/tcp` and `8554/tcp` are closed.
- P2-03 ONVIF testing is also low-probability because `3702/udp` is closed.
- P2-04 should include `8800/tcp` as a proprietary binary service, not just HTTP/MJPEG.
- If P2 cannot obtain a local video stream, the project should continue toward UART/firmware evidence before any firmware modification.

## Recommended Next Step

Proceed to P2-01 with a fuller TCP port scan and careful service inventory.
