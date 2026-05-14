# UART Connection Notes

## Safety Rules

- 先确认 GND。
- 再测 RX/TX 空闲电平。
- USB-TTL 不给摄像头供电。
- 第一轮只接 GND 和摄像头 TX -> USB-TTL RX。
- 确认能稳定读取 boot log 后，再连接 USB-TTL TX -> 摄像头 RX。
- 禁止使用 5V TTL。

## Connection

| Camera Pad | USB-TTL Pin | Notes |
|---|---|---|
| GND | GND | 待确认 |
| TX | RX | 摄像头输出 |
| RX | TX | 后续再接 |
| VCC | 不接 | 禁止供电 |
