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

---

## Experiment ID: EXP-0005

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P0-06 |
| Goal | Save pcapng captures for boot, App preview, and App PTZ/control scenarios |
| Device State | Camera online through Windows Mobile Hotspot |
| Network State | Camera on 192.168.137.177, phone on 192.168.137.29, gateway on 192.168.137.1 |
| Tools Used | tshark / Wireshark / Npcap |
| Related Files | 01_network_capture/pcap_raw/*.pcapng / 01_network_capture/capture_manifest.md |

### Steps

1. Confirmed Wireshark/tshark capture interface `本地连接* 10`.
2. Captured camera boot and online behavior for 120 seconds.
3. Captured App preview behavior for 60 seconds.
4. Captured App PTZ/control behavior for 60 seconds.
5. Extracted initial IP conversation summaries and DNS observations from the saved pcapng files.
6. Recorded the capture index in `01_network_capture/capture_manifest.md`.

### Observations

- Boot capture saved as `20260514_2104_boot_online_camera_192.168.137.177.pcapng`, 288 packets, 75416 bytes.
- App preview capture saved as `20260514_app_preview_camera_192.168.137.177.pcapng`, 117 packets, 43360 bytes.
- App PTZ/control capture saved as `20260514_app_ptz_camera_192.168.137.177.pcapng`, 79 packets, 31256 bytes.
- DNS observations include `svc.av380.net`, `alivetype.av380.net`, `alarmserverlist.av380.net`, `devota.av380.net`, `logs.av380.net`, `ipc79.w390.net`, `regipc4379.av380.net`, and `push2.av380.net`.
- No direct camera-to-phone traffic was identified in the high-level conversation summaries.

### Results

- P0-06 is complete for the initial online, App preview, and App PTZ/control scenarios.
- Raw pcapng files are saved locally under `01_network_capture/pcap_raw/`.
- Raw capture files are intentionally ignored by Git.
- DNS and conversation evidence is sufficient to enter P1-01/P1-02/P1-03.

### Problems

- Blocked-internet capture is not included yet; it should be handled during P1-06 after baseline analysis.
- PTZ command semantics are not decoded yet; this belongs to P1/P2 analysis.

### Next Step

- Continue with P1-01: analyze the saved boot pcap and extract the boot-stage network behavior.

---

## Experiment ID: EXP-0006

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-01 |
| Goal | Analyze the saved camera boot pcap and extract boot-stage network behavior |
| Device State | Analysis performed on saved boot pcap |
| Network State | Baseline online boot capture from Windows Mobile Hotspot |
| Tools Used | tshark |
| Related Files | 01_network_capture/pcap_raw/20260514_2104_boot_online_camera_192.168.137.177.pcapng / 01_network_capture/boot_capture_analysis.md |

### Steps

1. Loaded the saved boot pcapng file with tshark.
2. Extracted protocol hierarchy statistics.
3. Extracted IPv4, TCP, and UDP conversation summaries.
4. Extracted DNS, DHCP, NTP, HTTP, TLS, and key transport events in relative-time order.
5. Wrote the P1-01 analysis to `01_network_capture/boot_capture_analysis.md`.

### Observations

- The boot pcap contains 288 frames.
- Main protocols include TCP, UDP/DNS, DHCP, NTP, HTTP JSON, TLSv1.2, ICMP, and ARP.
- DHCP Offer and ACK from `192.168.137.1` appear around 49.3s relative time.
- DNS resolution begins immediately after DHCP, including `ntp.sjtu.edu.cn` and several `av380.net` / `w390.net` domains.
- Plain HTTP JSON calls are visible to `svc.av380.net`, `alivetype.av380.net`, `alarmserverlist.av380.net`, `logs.av380.net`, and `push2.av380.net`.
- TLSv1.2 traffic uses SNI `devota.av380.net`.
- Custom UDP-like traffic is visible with `120.27.12.196`, including ports 8877, 9001, 7788, and 1341.

### Results

- P1-01 is complete.
- The boot capture is sufficient for P1-02 DNS analysis and P1-03 TCP/UDP flow analysis.
- Initial evidence indicates the camera performs cloud service discovery, time sync, log/meta reporting, and persistent/custom UDP communication during boot.

### Problems

- The capture starts with existing UDP traffic, so the first packet is not necessarily the first packet emitted by the camera after power-on.
- Some HTTP payload details may contain device identifiers and should be handled carefully.

### Next Step

- Continue with P1-02: analyze DNS requests and list primary cloud service domains.

---

## Experiment ID: EXP-0007

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-02 |
| Goal | Analyze DNS requests and identify primary cloud service domains |
| Device State | Analysis performed on saved pcap files |
| Network State | Baseline online boot, App preview, and App PTZ/control captures |
| Tools Used | tshark |
| Related Files | 01_network_capture/dns_analysis.md |

### Steps

1. Extracted DNS requests and responses from the boot capture.
2. Extracted DNS requests and responses from the App preview capture.
3. Extracted DNS requests and responses from the App PTZ/control capture.
4. Compared domain appearances across scenarios.
5. Cross-checked DNS names against observed HTTP and TLS traffic where possible.
6. Wrote the DNS analysis to `01_network_capture/dns_analysis.md`.

### Observations

- Main vendor domain family: `av380.net`.
- Additional IPC/cloud channel domain family: `w390.net`.
- Time sync uses `ntp.sjtu.edu.cn`.
- `ipc79.w390.net` appears in boot, preview, and PTZ/control captures.
- `devota.av380.net` appears in boot and preview captures and is used as TLS SNI.
- HTTP endpoints under `svc.av380.net`, `alivetype.av380.net`, `alarmserverlist.av380.net`, `logs.av380.net`, and `push2.av380.net` are visible in plaintext.

### Results

- P1-02 is complete.
- Primary cloud domains are identified and grouped by observed role.
- `ipc79.w390.net` and `devota.av380.net` should be prioritized in P1-03.

### Problems

- DNS analysis alone cannot prove exact application semantics.
- Some endpoint roles are inferred from domain names, paths, and scenario correlation; P1-03 should confirm via flow behavior.

### Next Step

- Continue with P1-03: analyze TCP and UDP communication flows.

---

## Experiment ID: EXP-0008

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-03 |
| Goal | Analyze TCP and UDP communication flows |
| Device State | Analysis performed on saved pcap files |
| Network State | Baseline online boot, App preview, and App PTZ/control captures |
| Tools Used | tshark |
| Related Files | 01_network_capture/communication_flow_analysis.md |

### Steps

1. Reviewed the current task sequence before continuing.
2. Confirmed no major adjustment is required before P1-03.
3. Extracted TCP and UDP conversation summaries from boot, preview, and PTZ captures.
4. Focused detailed packet timing on `120.27.12.196` / `ipc79.w390.net`.
5. Compared HTTP, TLS, and custom UDP traffic across scenarios.
6. Wrote the analysis to `01_network_capture/communication_flow_analysis.md`.

### Observations

- `120.27.12.196` appears in boot, preview, and PTZ/control captures.
- `120.27.12.196` uses TCP 1340 and UDP 8877, 9001, 7788, and 1341.
- TCP 1340 sessions are very short and close immediately.
- UDP 8877 becomes the dominant repeated flow and looks keepalive-like.
- Plain HTTP cloud service endpoints are visible under `av380.net`.
- TLSv1.2 traffic uses SNI `devota.av380.net`.
- No direct camera-to-phone TCP/UDP path was identified in the current summaries.

### Results

- P1-03 is complete.
- Remote IPs, ports, and broad protocol types are listed.
- `ipc79.w390.net` / `120.27.12.196` is the highest-priority endpoint for later control/relay behavior analysis.

### Problems

- Preview and PTZ captures are short baseline captures; structured repeat captures would improve confidence.
- Packet payload semantics for the custom UDP flows are not decoded.

### Next Step

- Continue with P1-04 and P1-05 as validation captures, or proceed to P1-06 if the goal is to test offline/local behavior next.
