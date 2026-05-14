# P2-03 ONVIF Test Results

Stage: P2-03

Date: 2026-05-14

## Goal

Test whether the camera exposes a local ONVIF interface or responds to ONVIF WS-Discovery.

Camera:

| Item | Value |
| --- | --- |
| IP | `192.168.137.177` |
| MAC | `58:c5:87:9a:ab:97` |
| Network | Windows Mobile Hotspot `192.168.137.0/24` |

## Tests Performed

### UDP Discovery / ONVIF Related Ports

Raw output:

```text
03_video_stream_test/onvif_tests/20260514_p2_03_onvif_udp_tcp_related.txt
03_video_stream_test/onvif_tests/20260514_p2_03_onvif_udp_tcp_related.xml
```

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sU -Pn -n --reason -p 3702,1900,5353,8899,5000,5001,8080,80 -oN '03_video_stream_test\onvif_tests\20260514_p2_03_onvif_udp_tcp_related.txt' -oX '03_video_stream_test\onvif_tests\20260514_p2_03_onvif_udp_tcp_related.xml' 192.168.137.177
```

Result:

| Port | State | Notes |
| ---: | --- | --- |
| 3702/udp | closed | WS-Discovery / ONVIF discovery not listening |
| 1900/udp | closed | SSDP/UPnP not listening |
| 5353/udp | closed | mDNS not listening |
| 8899/udp | closed | Common vendor discovery port closed |
| 5000/udp | closed | Common UPnP/alternate service closed |
| 5001/udp | closed | Alternate service closed |
| 8080/udp | closed | Alternate service closed |
| 80/udp | closed | Not useful for ONVIF |

### Common ONVIF HTTP/TCP Ports

Raw output:

```text
03_video_stream_test/onvif_tests/20260514_p2_03_onvif_tcp_related.txt
03_video_stream_test/onvif_tests/20260514_p2_03_onvif_tcp_related.xml
```

Command:

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p 80,8080,8899,5000,5001,8000,8001,8081,8088,8090 -oN '03_video_stream_test\onvif_tests\20260514_p2_03_onvif_tcp_related.txt' -oX '03_video_stream_test\onvif_tests\20260514_p2_03_onvif_tcp_related.xml' 192.168.137.177
```

Result:

| Port | State | Notes |
| ---: | --- | --- |
| 80/tcp | closed | No standard ONVIF HTTP endpoint |
| 8080/tcp | closed | No common alternate ONVIF HTTP endpoint |
| 8899/tcp | closed | No common vendor/ONVIF endpoint |
| 5000/tcp | closed | No common ONVIF/UPnP endpoint |
| 5001/tcp | closed | No common alternate endpoint |
| 8000/tcp | closed | No common alternate endpoint |
| 8001/tcp | closed | No common alternate endpoint |
| 8081/tcp | closed | No common alternate endpoint |
| 8088/tcp | closed | No common alternate endpoint |
| 8090/tcp | closed | No common alternate endpoint |

### Manual WS-Discovery Probe

A SOAP WS-Discovery Probe was sent to both:

```text
239.255.255.250:3702
192.168.137.177:3702
```

Result:

```text
sent_probe_to=239.255.255.250:3702 bytes=628
sent_probe_to=192.168.137.177:3702 bytes=628
responses=0
```

Interpretation:

- No ONVIF WS-Discovery response was received.
- This matches the `3702/udp closed` result.

## P2-03 Result

P2-03 is complete.

Current conclusion:

1. The camera does not expose a detectable ONVIF WS-Discovery service on `3702/udp`.
2. The camera did not respond to a manual WS-Discovery Probe.
3. Common ONVIF HTTP/TCP ports are closed.
4. No local ONVIF interface was found.

## Next Step Recommendation

Proceed to P2-04.

P2-04 should focus on:

- HTTP/MJPEG checks for common paths, even though `80/tcp` and `8080/tcp` are closed.
- Direct checks against the discovered open private ports:
  - `192.168.137.177:8800/tcp`
  - `192.168.137.177:9800/tcp`
- Binary/proprietary protocol observation rather than assuming standard RTSP/ONVIF.
