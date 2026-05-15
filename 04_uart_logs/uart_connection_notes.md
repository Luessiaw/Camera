# UART Connection Notes

## Safety Rules

- 先确认 GND。
- 再测 RX/TX 空闲电平。
- USB-TTL 不给摄像头供电。
- 第一轮只接 GND 和摄像头 TX -> USB-TTL RX。
- 确认能稳定读取 boot log 并完成风险评估后，再考虑连接 USB-TTL TX -> 摄像头 RX。
- 禁止使用 5V TTL。

## P3-01 GND Continuity Result

Date: 2026-05-15

Camera power state: powered off.

The following points beeped against the large copper area in continuity mode:

| Point | Interpretation |
| --- | --- |
| Power negative pad | GND confirmed |
| U10 pad | On GND net candidate |
| Pad below `v1.0` marking | On GND net candidate |
| Silver solder matrix below `J5` | On GND net candidate |

Result:

- P3-01 is complete at the practical level.
- The large copper area and power negative pad can be used as the GND reference for P3-02 voltage measurements.
- Do not assume U10 / v1.0 / J5 nearby pads are UART just because they are on GND; they are only confirmed as ground-net points.

## P3-02 UART Idle Voltage Result

Date: 2026-05-15

Camera power state: powered on with the original camera power supply.

Voltage reference: confirmed GND net from P3-01.

| Pad | Observed Voltage | Interpretation |
| --- | --- | --- |
| RX | Rose to about 3.23 V after power-on and stayed stable within about +/-0.01 V | Likely 3.3 V TTL UART RX idle-high input |
| TX | Rose to about 3.29 V after power-on, with multiple brief drops below 3 V | Likely 3.3 V TTL UART TX idle-high output with boot log activity |

Result:

- P3-02 is complete at the practical level.
- The UART appears to use 3.3 V TTL levels.
- The observed TX voltage drops are consistent with serial output during boot.
- Do not connect any 5 V TTL adapter.
- Continue with read-only wiring only: camera GND -> USB-TTL GND, camera TX -> USB-TTL RX.

## Connection

| Camera Pad | USB-TTL Pin | Notes |
|---|---|---|
| GND | GND | Use large copper area or power negative pad as confirmed GND reference |
| TX | RX | Camera output; likely active based on P3-02 voltage drops |
| RX | TX | Do not connect during read-only phase |
| VCC | 不接 | 禁止供电 |
