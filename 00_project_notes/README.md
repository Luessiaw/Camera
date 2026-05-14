# xiaovv_camera_local

## 1. Project Goal

将 xiao vv 家用摄像头从云端依赖模式改造为本地可控模式，使其尽可能通过个人服务器完成视频接入、存储、目标检测、移动跟踪和远程访问。

## 2. Target Functions

- 白天彩色成像
- 夜间黑白成像
- 本地视频流接入
- 云台双方向控制
- 本地目标检测与移动跟踪
- 低功耗运行策略
- 长期稳定运行
- 可备份、可恢复、可维护

## 3. Current Architecture

- Domain: Cloudflare
- Server: old laptop, planned Ubuntu Server
- Private Network: Tailscale
- Temporary Debug Platform: Windows PC
- Camera: xiao vv camera
- Camera SoC: ANYKA AK3918EV300
- SPI Flash: 250H128DHIQ
- Debug Pads: RX, TX, possible GND

## 4. Main Principle

优先级：

1. 网络层接管
2. 本地视频流接入
3. 串口只读分析
4. 固件完整备份
5. 最小固件修改
6. 服务器侧 AI 与自动化
7. 长期稳定运行

原则：

- 能不刷机就不刷机
- 能保留原厂底层驱动就保留
- 刷机前必须完成 Flash 备份与恢复验证
- 摄像头服务不直接暴露公网
- 管理访问优先使用 Tailscale
