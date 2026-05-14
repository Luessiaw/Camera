# Device Information

## 1. Basic Info

| Item | Value |
| --- | --- |
| Device Name | xiao vv camera |
| Model | 待确认 |
| Purchase Date | 待填写 |
| App Name | 待填写 |
| Power Supply | 待确认 |
| WiFi Type | 待确认 |
| Night Vision | Yes / No |
| PTZ | Yes, two-axis |

## 2. Hardware Info

| Component | Information |
| --- | --- |
| SoC | ANYKA AK3918EV300 |
| SPI Flash | 250H128DHIQ |
| Flash Capacity | 待确认 |
| RAM | 待确认 |
| UART Pads | RX, TX, possible GND |
| Motor Driver | 待确认 |
| IR LED Control | 待确认 |
| IR-cut Filter | 待确认 |

## 3. Board Notes

- RX pad location:
- TX pad location:
- GND candidate:
- Measured voltage:
- Photos saved in:

## 4. Network Info

| Item | Value |
| --- | --- |
| MAC Address | 58:c5:87:9a:ab:97 |
| IP Address | 192.168.137.177 |
| Hostname | 未知 |
| Open Ports | 待填写 |
| Cloud Domains | 待填写 |

## 5. Phone Info

| Item | Value |
| --- | --- |
| MAC Address | 3a:1c:64:3b:ce:af |
| IP Address | 192.168.137.29 |
| Hostname | LuessiawHonor |
| Open Ports | 待填写 |
| Cloud Domains | 待填写 |

## 5. Known Risks

- UART 电平未知，必须先测量。
- 禁止 USB-TTL 5V 接入摄像头。
- USB-TTL 不应向摄像头供电。
- 刷机前必须备份 SPI Flash。
- 未验证恢复前不得修改 Flash。

## P0-02 Network Verification

| Item | Value |
| --- | --- |
| Network Type | Windows Mobile Hotspot |
| Hotspot Gateway | 192.168.137.1 |
| Camera IP Address | 192.168.137.177 |
| Camera MAC Address | 58:c5:87:9a:ab:97 |
| Camera Hostname | Unknown |
| Phone IP Address | 192.168.137.29 |
| Phone MAC Address | 3a:1c:64:3b:ce:af |
| Phone Hostname | LuessiawHonor |
| Verification Status | Camera and phone are connected to the Windows hotspot subnet |

## P0-05 Startup and App Behavior

| Item | Value |
| --- | --- |
| Observation Time | 2026-05-14 21:04:20 +08:00 |
| Power-on Time | 2026-05-14 21:04:20 +08:00 |
| Board Indicator | Red LED turns on immediately and stays solid |
| Voice Prompt 1 | About 15s after power-on: "欢迎使用" |
| Voice Prompt 2 | About 25s after power-on: "网络连接中" |
| Voice Prompt 3 | About 30s after power-on: "网络连接完成" |
| App Preview Result | Successful |
| App Preview Load Time | About 4s after tapping preview |
| Night Vision Control | No manual night-vision option observed in the app; likely automatic |
| Traffic Observation | Wireshark showed camera communication with 192.168.137.1 and multiple external IP addresses |
| Phone Direct Traffic | No direct camera-to-phone communication observed during preview |
