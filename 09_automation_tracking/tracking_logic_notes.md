# Tracking Logic Notes

## Goal

由服务器完成目标检测与跟踪决策，摄像头只负责视频采集和云台执行。

## Basic Logic

1. 服务器接收视频流。
2. Frigate / Motion 检测目标。
3. Python 服务读取目标位置。
4. 判断目标是否偏离画面中心。
5. 发送 PTZ 控制命令。
6. 设置冷却时间，避免频繁抖动。

## PTZ Interface

| Direction | Command / API | Notes |
|---|---|---|
| Left | 待确认 |  |
| Right | 待确认 |  |
| Up | 待确认 |  |
| Down | 待确认 |  |
| Stop | 待确认 |  |
