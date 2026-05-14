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
