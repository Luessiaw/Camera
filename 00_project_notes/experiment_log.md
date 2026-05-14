# Experiment Log

---

## Experiment ID: EXP-0001

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw |
| Stage | P0-04 |
| Goal | 建立项目文件夹与记录模板 |
| Device State | 未连接 |
| Network State | 未建立 |
| Tools Used | Python |
| Related Files | 本项目目录结构 |

### Steps

1. 运行 Python 脚本。
2. 创建项目根目录。
3. 创建阶段文件夹。
4. 创建 README、project_goal、device_info、experiment_log、risk_notes、command_cheatsheet 等模板文件。

### Observations

- 项目结构已建立。
- 后续实验文件将按阶段存储。

### Results

- P0-04 初步完成。

### Problems

- 暂无。

### Next Step

- 等待 USB WiFi 网卡到货后执行 P0-01/P0-02。

---

## Experiment ID: EXP-0002

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw |
| Stage | P0-02 |
| Goal | Establish an isolated Windows Mobile Hotspot test network for the camera and phone |
| Device State | Camera connected to Windows Mobile Hotspot |
| Network State | Camera and phone are on the 192.168.137.0/24 hotspot subnet |
| Tools Used | Windows Mobile Hotspot / Windows network device list / ARP observation |
| Related Files | 00_project_notes/device_info.md |

### Steps

1. Enabled Windows Mobile Hotspot on the Windows PC.
2. Connected the xiao vv camera to the hotspot.
3. Connected the phone to the same hotspot.
4. Identified and recorded the camera IP address and MAC address.
5. Identified and recorded the phone IP address and MAC address.

### Observations

- Camera IP: 192.168.137.177
- Camera MAC: 58:c5:87:9a:ab:97
- Phone IP: 192.168.137.29
- Phone MAC: 3a:1c:64:3b:ce:af
- Hotspot gateway: 192.168.137.1

### Results

- P0-02 isolation setup is complete at the project-record level.
- Camera and phone are both connected to the Windows Mobile Hotspot.
- Basic network identifiers required for P0-05 and P1 capture work have been recorded.

### Problems

- Camera hostname is currently unknown.
- Open ports and cloud domains have not been checked yet.

### Next Step

- Continue with P0-03: install and verify Wireshark, Npcap, nmap, VLC, and ffmpeg/ffprobe.
