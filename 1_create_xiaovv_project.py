from pathlib import Path
from datetime import datetime

# ============================================================
# xiao vv camera local project initializer
# 用途：
#   自动创建项目文件夹与 Markdown 记录模板。
#
# 使用方法：
#   1. 修改 PROJECT_ROOT 为你希望保存项目的位置。
#   2. 在 PowerShell 或 CMD 中运行：
#      python create_xiaovv_project.py
# ============================================================

# Windows 默认路径：用户 Documents/Projects/xiaovv_camera_local
# PROJECT_ROOT = Path.home() / "Documents" / "Projects" / "xiaovv_camera_local"
PROJECT_ROOT = Path(r"C:\Users\Luessiaw\Nutstore\1\Thoughts\Others\20260514摄像头破解")

FOLDERS = [
    "00_project_notes",

    "01_network_capture",
    "01_network_capture/pcap_raw",
    "01_network_capture/pcap_filtered",
    "01_network_capture/screenshots",

    "02_network_scan",
    "02_network_scan/nmap",
    "02_network_scan/arp",

    "03_video_stream_test",
    "03_video_stream_test/rtsp_tests",
    "03_video_stream_test/onvif_tests",
    "03_video_stream_test/http_stream_tests",
    "03_video_stream_test/ffmpeg_logs",
    "03_video_stream_test/screenshots",

    "04_uart_logs",
    "04_uart_logs/raw_logs",
    "04_uart_logs/cleaned_logs",

    "05_firmware_backup",
    "05_firmware_backup/flash_dump_raw",
    "05_firmware_backup/flash_dump_verified",
    "05_firmware_backup/hash_records",
    "05_firmware_backup/chip_info",

    "06_firmware_analysis",
    "06_firmware_analysis/binwalk_output",
    "06_firmware_analysis/extracted_rootfs",
    "06_firmware_analysis/strings_output",
    "06_firmware_analysis/service_analysis",
    "06_firmware_analysis/ptz_analysis",

    "07_modified_firmware",
    "07_modified_firmware/patches",
    "07_modified_firmware/repack_output",
    "07_modified_firmware/test_versions",

    "08_server_deployment",
    "08_server_deployment/docker",
    "08_server_deployment/frigate",
    "08_server_deployment/motion",
    "08_server_deployment/mqtt",
    "08_server_deployment/tailscale",
    "08_server_deployment/cloudflare",

    "09_automation_tracking",
    "09_automation_tracking/python_service",
    "09_automation_tracking/ptz_control",
    "09_automation_tracking/detection_tests",

    "10_long_term_operation",
    "10_long_term_operation/systemd",
    "10_long_term_operation/watchdog",
    "10_long_term_operation/logrotate",
    "10_long_term_operation/backup_strategy",
    "10_long_term_operation/uptime_logs",

    "90_references",
    "90_references/datasheets",

    "99_archive",
    "99_archive/old_notes",
    "99_archive/failed_attempts",
    "99_archive/deprecated_configs",
]


def build_files() -> dict[str, str]:
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "00_project_notes/README.md": """# xiaovv_camera_local

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
""",

        "00_project_notes/project_goal.md": """# Project Goal

## 总目标

构建个人数据基础设施中的本地摄像头系统，使 xiao vv 摄像头尽可能脱离厂商云端，通过本地服务器完成视频流接入、存储、识别、通知与自动跟踪。

## 阶段目标

| 阶段 | 目标 |
|---|---|
| P0 | 建立实验环境与记录体系 |
| P1 | 分析摄像头网络行为 |
| P2 | 尝试本地视频流接管 |
| P3 | 串口只读分析 |
| P4 | 固件备份与恢复验证 |
| P5 | 最小固件修改 |
| P6 | 服务器侧功能接管 |
| P7 | 长期稳定运行 |

## 当前原则

- 优先尝试网络层接管。
- 如果能直接获得本地视频流，暂不刷机。
- 串口阶段先只读，不急于输入命令。
- 固件修改前必须完成 SPI Flash 完整备份与恢复验证。
""",

        "00_project_notes/device_info.md": """# Device Information

## 1. Basic Info

| Item | Value |
|---|---|
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
|---|---|
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
|---|---|
| MAC Address | 待填写 |
| IP Address | 待填写 |
| Hostname | 待填写 |
| Open Ports | 待填写 |
| Cloud Domains | 待填写 |

## 5. Known Risks

- UART 电平未知，必须先测量。
- 禁止 USB-TTL 5V 接入摄像头。
- USB-TTL 不应向摄像头供电。
- 刷机前必须备份 SPI Flash。
- 未验证恢复前不得修改 Flash。
""",

        "00_project_notes/experiment_log.md": f"""# Experiment Log

---

## Experiment ID: EXP-0001

| Item | Value |
|---|---|
| Date | {today} |
| Operator | Baichuan |
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
""",

        "00_project_notes/risk_notes.md": """# Risk Notes

## 1. Network Risks

- 摄像头不应直接接入家庭主网。
- 摄像头不应直接暴露到公网。
- 未明确协议前，不允许随意开放端口。
- 调试阶段建议使用隔离热点。

## 2. UART Risks

- 未确认电平前，不连接 USB-TTL。
- USB-TTL 不向摄像头供电。
- 优先只读 boot log，不输入命令。
- 禁止使用 5V TTL。
- TX/RX 应交叉连接。

## 3. Firmware Risks

- 未完整备份 SPI Flash 前，不修改固件。
- 未验证写回恢复前，不刷机。
- 原始固件至少保存三份。
- 修改固件时采用最小修改原则。
- 不建议一开始替换完整系统。

## 4. Privacy Risks

- 视频数据只保存在本地服务器。
- 远程访问优先使用 Tailscale。
- 不将摄像头管理页面暴露公网。
- Cloudflare 仅用于必要 Web 服务，不建议直接暴露摄像头后台。
""",

        "01_network_capture/wireshark_notes.md": """# Wireshark Notes

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
""",

        "02_network_scan/port_scan_results.md": """# Port Scan Results

## Device IP

```text
待填写
```

## Quick Scan

Command:

```bash
nmap -sV <camera_ip>
```

Result:

```text
待填写
```

## Full Port Scan

Command:

```bash
nmap -p- <camera_ip>
```

Result:

```text
待填写
```

## Summary

| Port | Protocol | Service | Status | Notes |
|---|---|---|---|---|
""",

        "02_network_scan/commands_used.md": """# Commands Used

## Windows

```powershell
ipconfig /all
arp -a
ping <camera_ip>
```

## nmap

```bash
nmap -sV <camera_ip>
nmap -p- <camera_ip>
nmap -sV -O <camera_ip>
```

## ffmpeg / ffprobe

```bash
ffprobe rtsp://<camera_ip>:554/<path>
ffmpeg -i rtsp://<camera_ip>:554/<path> -f null -
```
""",

        "03_video_stream_test/stream_test_results.md": """# Stream Test Results

## RTSP Test

| Path | Tool | Result | Notes |
|---|---|---|---|
| rtsp://<camera_ip>:554/live | VLC / ffprobe | 待测试 |  |
| rtsp://<camera_ip>:554/h264 | VLC / ffprobe | 待测试 |  |
| rtsp://<camera_ip>:554/stream1 | VLC / ffprobe | 待测试 |  |
| rtsp://<camera_ip>:554/stream2 | VLC / ffprobe | 待测试 |  |

## ONVIF Test

| Tool | Result | Notes |
|---|---|---|
| ONVIF Device Manager | 待测试 |  |

## HTTP Stream Test

| URL | Result | Notes |
|---|---|---|
| http://<camera_ip>/ | 待测试 |  |
""",

        "04_uart_logs/bootlog_analysis.md": """# Bootlog Analysis

## UART Settings

| Item | Value |
|---|---|
| Baud Rate | 待确认 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Flow Control | None |

## Boot Information

| Item | Value |
|---|---|
| Bootloader | 待确认 |
| Kernel Version | 待确认 |
| RootFS Type | 待确认 |
| MTD Partitions | 待确认 |
| Login Prompt | Yes / No |
| Shell Access | Yes / No |

## Notes

```text
待填写
```
""",

        "04_uart_logs/uart_connection_notes.md": """# UART Connection Notes

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
""",

        "05_firmware_backup/recovery_notes.md": """# Recovery Notes

## Flash Backup

| Dump File | SHA256 | Notes |
|---|---|---|
| flash_dump_01_raw.bin | 待填写 |  |
| flash_dump_02_raw.bin | 待填写 |  |
| flash_dump_03_raw.bin | 待填写 |  |

## Recovery Procedure

1. 断电。
2. 连接 SPI Flash 编程器。
3. 读取并确认芯片 ID。
4. 写入原始固件镜像。
5. 校验写入内容。
6. 断开编程器。
7. 摄像头上电。
8. 检查 boot log 和网络行为。

## Notes

```text
待填写
```
""",

        "06_firmware_analysis/firmware_analysis_notes.md": """# Firmware Analysis Notes

## Firmware Image

| Item | Value |
|---|---|
| Image File | 待填写 |
| Size | 待填写 |
| SHA256 | 待填写 |

## binwalk Result

```text
待填写
```

## RootFS

| Item | Value |
|---|---|
| Type | 待确认 |
| Extracted Path | 待填写 |

## Interesting Files

| File | Possible Function | Notes |
|---|---|---|

## Services

| Service / Process | Function | Notes |
|---|---|---|

## Cloud Related

| File / Domain / Process | Notes |
|---|---|

## Video Related

| File / Process | Notes |
|---|---|

## PTZ Related

| File / Process / Device Node | Notes |
|---|---|
""",

        "07_modified_firmware/rollback_plan.md": """# Rollback Plan

## Principle

任何固件修改都必须能回滚到原始状态。

## Rollback Assets

| Asset | Path | Notes |
|---|---|---|
| Original Flash Dump | 待填写 |  |
| Hash Record | 待填写 |  |
| Programmer Software | 待填写 |  |
| Wiring Photo | 待填写 |  |

## Rollback Steps

1. 断电。
2. 使用编程器连接 SPI Flash。
3. 写回原始 Flash 镜像。
4. 校验写入。
5. 摄像头重新上电。
6. 观察 boot log。
7. 验证网络与 App 行为。
""",

        "08_server_deployment/server_setup_notes.md": """# Server Setup Notes

## Server Info

| Item | Value |
|---|---|
| Machine | Old laptop |
| OS | Ubuntu Server |
| Hostname | 待填写 |
| IP | 待填写 |
| Tailscale IP | 待填写 |

## Planned Services

| Service | Function | Access Method |
|---|---|---|
| Frigate / Motion | NVR and detection | Tailscale |
| MQTT | Event communication | LAN / Tailscale |
| Python PTZ Service | Auto tracking | LAN |
| Cloudflare | Domain / limited web services | Public as needed |

## Notes

```text
待填写
```
""",

        "09_automation_tracking/tracking_logic_notes.md": """# Tracking Logic Notes

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
""",

        "10_long_term_operation/maintenance_notes.md": """# Maintenance Notes

## Long Term Operation

| Item | Method | Notes |
|---|---|---|
| Auto Start | systemd | 待配置 |
| Health Check | watchdog / cron | 待配置 |
| Log Rotation | logrotate | 待配置 |
| Video Retention | Frigate retention | 待配置 |
| Backup | rsync / external drive | 待配置 |

## Regular Check

| Frequency | Task |
|---|---|
| Daily | 检查服务是否在线 |
| Weekly | 检查磁盘空间和日志 |
| Monthly | 备份配置文件 |
""",

        "90_references/useful_links.md": """# Useful Links

## Vendor / Device

- 待填写

## ANYKA / SoC

- 待填写

## Tools

- Wireshark
- nmap
- ffmpeg
- VLC
- ONVIF Device Manager
- binwalk
- flashrom
- Frigate
- Tailscale
- Cloudflare

## Notes

```text
待填写
```
""",

        "90_references/command_cheatsheet.md": """# Command Cheatsheet

## 1. Windows Network

### 查看网络配置

```powershell
ipconfig /all
```

### 查看 ARP 表

```powershell
arp -a
```

### 测试连接

```powershell
ping <camera_ip>
```

## 2. nmap

### 快速扫描

```bash
nmap -sV <camera_ip>
```

### 全端口扫描

```bash
nmap -p- <camera_ip>
```

### 常见服务扫描

```bash
nmap -sV -O <camera_ip>
```

## 3. ffmpeg / ffprobe

### 测试 RTSP

```bash
ffprobe rtsp://<camera_ip>:554/<path>
```

```bash
ffmpeg -i rtsp://<camera_ip>:554/<path> -f null -
```

## 4. UART

### 常见串口参数

```text
115200 8N1
57600 8N1
38400 8N1
9600 8N1
```

## 5. Linux Later

### 查看 IP

```bash
ip addr
```

### 抓包

```bash
sudo tcpdump -i wlan0 -w capture.pcapng
```
""",
    }


def create_project_structure(project_root: Path, overwrite_files: bool = False) -> None:
    """
    创建项目文件夹和模板文件。

    Parameters
    ----------
    project_root:
        项目根目录。
    overwrite_files:
        是否覆盖已经存在的模板文件。
        默认 False，避免误删你已经写好的笔记。
    """

    print(f"Project root: {project_root}")

    project_root.mkdir(parents=True, exist_ok=True)

    for folder in FOLDERS:
        folder_path = project_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR ] {folder_path}")

    files = build_files()

    for relative_path, content in files.items():
        file_path = project_root / relative_path

        if file_path.exists() and not overwrite_files:
            print(f"[SKIP] {file_path} already exists")
            continue

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"[FILE] {file_path}")

    print()
    print("Done.")
    print("项目文件夹与模板文件已创建。")
    print("注意：默认不会覆盖已有文件。如需覆盖，请将 overwrite_files=True。")


if __name__ == "__main__":
    create_project_structure(PROJECT_ROOT, overwrite_files=False)
