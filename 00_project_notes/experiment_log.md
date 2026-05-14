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

---

## Experiment ID: EXP-0003

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw |
| Stage | P0-03 |
| Goal | Install and verify packet capture and network analysis tools |
| Device State | Camera remains connected to Windows Mobile Hotspot |
| Network State | Windows hotspot subnet is active at 192.168.137.0/24 |
| Tools Used | Wireshark / Npcap / nmap |
| Related Files | 01_network_capture/wireshark_notes.md |

### Steps

1. Installed Wireshark.
2. Installed Npcap.
3. Confirmed nmap is available on the Windows PC.
4. Confirmed Wireshark can see the hotspot capture interface.

### Observations

- Camera IP remains 192.168.137.177.
- Phone IP remains 192.168.137.29.
- Hotspot gateway remains 192.168.137.1.
- Wireshark/tshark capture interface for the hotspot is `本地连接* 10`.

### Results

- P0-03 is complete at the project-record level.

### Problems

- `wireshark.exe` and `tshark.exe` may not be in the shell PATH, but `tshark.exe` exists under `C:\Program Files\Wireshark\`.

### Next Step

- Continue with P0-05: record camera MAC, IP, startup timing, and App behavior.

---

## Experiment ID: EXP-0004

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw |
| Stage | P0-05 |
| Goal | Record camera MAC, IP, startup timing, and App behavior |
| Device State | Camera successfully boots and comes online through the Windows Mobile Hotspot |
| Network State | Camera communicates through hotspot gateway and external IPs; no direct phone traffic observed |
| Tools Used | Windows Mobile Hotspot / Wireshark / App observation |
| Related Files | 00_project_notes/device_info.md / 01_network_capture/wireshark_notes.md |

### Steps

1. Kept the camera and phone connected to the Windows Mobile Hotspot.
2. Started a Wireshark observation on the hotspot interface.
3. Powered on the camera at 2026-05-14 21:04:20 +08:00.
4. Observed board LED and voice prompts during boot.
5. Opened the camera preview in the phone App after the device reported network connection completion.
6. Checked whether the App exposes night-vision controls.
7. Observed whether camera traffic goes directly to the phone.

### Observations

- Power-on time: 2026-05-14 21:04:20 +08:00.
- Red indicator LED on the board turned on immediately and stayed solid.
- About 15 seconds after power-on, the camera played the voice prompt: "欢迎使用".
- About 25 seconds after power-on, the camera played the voice prompt: "网络连接中".
- About 30 seconds after power-on, the camera played the voice prompt: "网络连接完成".
- After tapping the camera preview in the App, live video appeared after about 4 seconds.
- The App did not show a manual night-vision toggle; night vision is likely automatic.
- Wireshark showed camera traffic with 192.168.137.1 and multiple external IP addresses.
- No direct camera-to-phone communication was observed during preview.

### Results

- P0-05 is complete at the project-record level.
- The camera's base network identity is recorded: 192.168.137.177 / 58:c5:87:9a:ab:97.
- The App preview path appears not to be direct camera-to-phone LAN streaming based on this observation.
- The traffic pattern supports prioritizing P1 DNS/TCP/UDP analysis before any firmware work.

### Problems

- Exact external IP addresses and domains were not extracted yet.
- No pcap file has been saved as project evidence yet; this belongs to P0-06.
- Night-vision control remains unconfirmed because the App exposes no manual switch.

### Next Step

- Continue with P0-06: save pcapng captures for boot, App preview, and later PTZ/control scenarios.
