# Wireshark Notes

## Capture Scenarios

| Scenario | File | Notes |
|---|---|---|
| Camera boot with internet access | 待填写 |  |
| Camera boot with internet blocked | 待填写 |  |
| App preview video | 待填写 |  |
| App PTZ control | 待填写 |  |
| App motion tracking | 待填写 |  |

## Important Filters

```text
dns
tcp
udp
ip.addr == <camera_ip>
tcp.stream eq <stream_id>
```

## Observed Domains

| Domain | IP | Port | Notes |
|---|---|---|---|

## Observed Connections

| Local IP | Remote IP | Protocol | Port | Notes |
|---|---|---|---|---|
| 192.168.137.177 | 192.168.137.1 | TBD | TBD | Camera communicates with Windows hotspot gateway during boot/preview |
| 192.168.137.177 | Multiple external IPs | TBD | TBD | Seen during App preview; exact IPs/domains to be extracted in P1 |

## P0-05 Traffic Notes

- Observation time: 2026-05-14 21:04:20 +08:00.
- Camera IP: 192.168.137.177.
- Phone IP: 192.168.137.29.
- During App preview, no direct camera-to-phone communication was observed.
- Camera traffic was observed with the hotspot gateway and multiple external IP addresses.
- Save full pcapng evidence in P0-06 before doing deeper DNS/TCP/UDP analysis.
