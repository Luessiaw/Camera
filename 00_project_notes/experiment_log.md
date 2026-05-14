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

---

## Experiment ID: EXP-0009

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-04 |
| Goal | Validate App preview traffic path |
| Device State | Camera online through Windows Mobile Hotspot |
| Network State | Camera on 192.168.137.177, phone on 192.168.137.29, gateway on 192.168.137.1 |
| Tools Used | tshark / Wireshark / phone App |
| Related Files | 01_network_capture/pcap_raw/20260514_app_preview_structured_camera_192.168.137.177.pcapng / 01_network_capture/app_preview_analysis.md |

### Steps

1. Started a 90-second structured capture on the Windows Mobile Hotspot interface.
2. Closed and reopened the App live preview during the capture window.
3. Kept the live preview running until the capture ended.
4. Extracted IP/TCP/UDP conversations.
5. Checked for direct traffic involving the phone IP `192.168.137.29`.
6. Compared the structured capture against the earlier preview baseline.

### Observations

- Structured preview capture saved as `20260514_app_preview_structured_camera_192.168.137.177.pcapng`.
- The capture contains 133 packets and is 54148 bytes.
- Main remote endpoints are `58.221.36.18`, `120.27.12.196`, `192.168.137.1`, and `17.253.116.125`.
- `devota.av380.net` appears as TLS SNI on `58.221.36.18:443`.
- `ipc79.w390.net` resolves to `120.27.12.196`.
- No packets involving the phone IP `192.168.137.29` were found in the camera-filtered capture.

### Results

- P1-04 is complete.
- App preview does not appear to use a direct camera-to-phone LAN stream.
- Preview-related camera traffic is consistent with vendor/cloud-mediated communication.

### Problems

- Capture confirms the camera side only; phone-side packet capture would be required to prove the complete App path.
- This does not rule out unused local services on the camera.

### Next Step

- Continue with P1-05: structured PTZ/control capture with explicit movement action timestamps.

---

## Experiment ID: EXP-0010

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-05 |
| Goal | Capture and analyze App PTZ/control traffic |
| Device State | Camera online through Windows Mobile Hotspot |
| Network State | Camera on 192.168.137.177, phone on 192.168.137.29, gateway on 192.168.137.1 |
| Tools Used | tshark / Wireshark / phone App |
| Related Files | 01_network_capture/pcap_raw/20260514_app_ptz_structured_camera_192.168.137.177.pcapng / 01_network_capture/app_ptz_analysis.md |

### Steps

1. Started a 120-second structured PTZ/control capture on the Windows Mobile Hotspot interface.
2. Planned manual actions at 10s, 20s, 30s, 40s, 50s, and 60s.
3. Extracted IP/TCP/UDP conversations from the saved pcapng file.
4. Checked for phone-to-camera direct traffic.
5. Focused analysis on `120.27.12.196` and local phone-to-camera traffic.

### Observations

- Structured PTZ capture saved as `20260514_app_ptz_structured_camera_192.168.137.177.pcapng`.
- The capture contains 122 packets and is 56704 bytes.
- `120.27.12.196` remains active during the PTZ/control window.
- The camera uses TCP 1340 and UDP 8877, 9001, 7788, and 1341 with `120.27.12.196`.
- A local phone-to-camera packet appears at 26.439911s: `192.168.137.29:39202 -> 192.168.137.177:8800`, TCP payload `bc000000000000000000000000000000`.
- This phone-to-camera packet is small and is not a video stream.

### Results

- P1-05 capture is complete.
- Initial analysis suggests PTZ/control may involve both a local TCP 8800 signal and the existing cloud IPC channel.
- Final action attribution is pending the manual operation log.

### Problems

- The exact success/failure and "连接中" timing for each direction action has not yet been recorded in this log.
- Camera-side capture cannot fully prove whether the phone-to-cloud path stalled.

### Next Step

- Add manual PTZ action results to `01_network_capture/app_ptz_analysis.md`.

### Manual Action Log Addendum

| Relative Time | Action | Result |
| ---: | --- | --- |
| 12s | Up | Success |
| 21s | Down | Success |
| 31-38s | Left | App showed "connecting"; video interrupted; motor moved after the stall |
| 40s | Right | Success |
| 50s | Left | Success |
| 60s | Right | Success |

### Final P1-05 Result

- P1-05 is complete.
- PTZ/control may involve both a local TCP 8800 signal and the existing cloud IPC channel.
- The App stall around 31-38s correlates with `ipc79.w390.net` cloud IPC refresh/re-setup timing.
- Camera-side UDP 8877 traffic continued during the stall window, so the camera network path did not fully stop.
- More repeated direction-specific captures would be required to map TCP 8800 payloads to exact PTZ directions.

### Updated Next Step

- Continue with P1-06: block public internet and observe offline/local behavior.

---

## Experiment ID: EXP-0011

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-06 |
| Goal | Block public internet and observe offline/local behavior |
| Device State | Camera connected to Windows Mobile Hotspot |
| Network State | Hotspot LAN stayed active; upstream internet was interrupted and later restored |
| Tools Used | tshark / Wireshark / Windows Mobile Hotspot / phone App |
| Related Files | 01_network_capture/pcap_raw/20260514_blocked_internet_camera_192.168.137.177.pcapng / 01_network_capture/blocked_internet_analysis.md |

### Steps

1. Started a camera-filtered capture on the Windows Mobile Hotspot interface.
2. Kept the camera online during the initial baseline window.
3. Interrupted the PC upstream internet path while keeping the hotspot active.
4. Attempted App interaction during the blocked-internet window.
5. Restored the PC upstream internet path.
6. Extracted conversation, DNS, TCP 8800, relay/media, and recovery evidence from the saved pcapng.
7. Added the manually observed App behavior timeline.

### Observations

- Capture saved as `20260514_blocked_internet_camera_192.168.137.177.pcapng`.
- Capture duration: 178.127818300 seconds.
- Packet count: 3865.
- File size: 1666268 bytes.
- During the blocked window, DNS lookups for `devota.av380.net`, `ipc79.w390.net`, `ntp.sjtu.edu.cn`, `ntp.av380.net`, and `p2pdispa.av380.net` returned `No such name`.
- Local hotspot/gateway traffic continued during the blocked window.
- A local camera-to-phone packet appeared at 63.148773800s: `192.168.137.177:8800 -> 192.168.137.29:43104`, TCP payload length 90 bytes, followed by a retransmission.
- The camera continued attempting cloud IPC and relay connections while upstream connectivity was failing.
- After recovery, large TCP 32100 flows appeared with `121.14.11.152` and `47.104.64.146`.
- `devota.av380.net` and `ipc79.w390.net` resolved successfully again after recovery.
- Manual observation timeline: preview was open at 0s; upstream Ethernet was disconnected around 40s; pressing a direction button around 50s moved the motor but the video image did not update; exiting and re-entering preview around 60s showed unable to connect; upstream Ethernet was restored around 120s and preview worked normally again.

### Results

- P1-06 packet capture and initial analysis are complete.
- The camera does not appear to become a fully standalone LAN device when public internet is blocked.
- The local TCP 8800 path is now confirmed in two P1 scenarios, but its exact semantics are not decoded yet.
- Existing-session PTZ/control can appear to work briefly after upstream internet is disconnected.
- Fresh preview setup and video update appear to depend on cloud/upstream connectivity.
- Recovery behavior strongly depends on cloud IPC/relay endpoints.

### Problems

- Manual App observation times are approximate rather than synchronized to packet timestamps.
- Camera-filtered capture cannot fully observe phone-to-cloud traffic.
- The TCP 8800 payload is not decoded.

### Next Step

- Continue with local service discovery and TCP 8800-focused checks in the next phase.

---

## Experiment ID: EXP-0012

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P1-07 |
| Goal | Determine whether a directly usable local video interface exists |
| Device State | Camera online on Windows Mobile Hotspot |
| Network State | Camera reachable at 192.168.137.177 |
| Tools Used | ping.exe / nmap / curl.exe |
| Related Files | 01_network_capture/local_video_interface_assessment.md |

### Steps

1. Reassessed the task sequence after P1-06.
2. Confirmed P1-07 should include active checks for common local video ports and TCP 8800.
3. Confirmed the camera is reachable with ICMP ping.
4. Scanned common TCP video/service ports.
5. Ran service fingerprinting against TCP 8800 and common video ports.
6. Checked common UDP discovery ports, including ONVIF WS-Discovery.
7. Sent a basic HTTP request to TCP 8800.

### Observations

- Camera ping succeeded with 1-2 ms latency and TTL 64.
- TCP 80, 443, 554, 8554, 8080, and 8899 were closed.
- TCP 8800 was open.
- Nmap identified TCP 8800 as `unknown-camera` / `V308 camera service`.
- UDP 3702, 1900, 5353, 8800, and 8899 were closed.
- HTTP probing TCP 8800 connected but returned an empty reply, so it is not a normal HTTP endpoint.

### Results

- P1-07 is complete at the initial local-interface level.
- No standard RTSP, HTTP/MJPEG, or ONVIF local video interface was found.
- A proprietary local camera service exists on TCP 8800.
- The follow-up task order does not need a major change, but P2-04 should explicitly include TCP 8800 proprietary protocol investigation.

### Problems

- This was a targeted initial scan, not a full port inventory.
- ffprobe/ffmpeg were not available in PATH during this check.
- TCP 8800 protocol semantics remain unknown.

### Next Step

- Continue to P2-01: perform a fuller port scan and service inventory.

---

## Experiment ID: EXP-0013

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P2-01 |
| Goal | Perform a fuller port scan and service inventory |
| Device State | Camera online on Windows Mobile Hotspot |
| Network State | Camera reachable at 192.168.137.177 |
| Tools Used | ping.exe / nmap / curl.exe / PowerShell TcpClient |
| Related Files | 02_network_scan/port_scan_results.md / 02_network_scan/nmap/*.txt / 02_network_scan/nmap/*.xml |

### Steps

1. Confirmed the camera was reachable by ICMP ping.
2. Ran a full TCP connect scan across all 65535 ports.
3. Ran a UDP top-100 scan.
4. Ran service fingerprinting against discovered TCP ports.
5. Re-scanned discovered TCP ports to check whether their state was stable.
6. Performed basic banner and HTTP-style probes against discovered TCP ports.
7. Recorded commands and results in `02_network_scan/`.

### Observations

- Full TCP scan found `25/tcp`, `110/tcp`, `143/tcp`, `8800/tcp`, and `9800/tcp` open.
- A quick rescan again showed the same five ports open.
- Service fingerprinting reported `8800/tcp` as `unknown-camera` / `V308 camera service`.
- Service fingerprinting reported `9800/tcp` as `davsrc?`.
- During service fingerprinting, `25/tcp`, `110/tcp`, and `143/tcp` appeared closed/reset rather than open.
- No initial banner was observed on any discovered TCP port.
- HTTP-style probes to `25/tcp`, `110/tcp`, and `143/tcp` connected and then reset.
- HTTP-style probes to `8800/tcp` and `9800/tcp` connected but returned an empty reply.
- UDP top-100 scan found no open UDP ports.

### Results

- P2-01 is complete.
- Stable useful candidates are `8800/tcp` and `9800/tcp`.
- `25/tcp`, `110/tcp`, and `143/tcp` are suspicious/unstable and should not be treated as standard mail services without stronger evidence.
- No standard local RTSP, HTTP/MJPEG, ONVIF, SSDP, or mDNS service was found.

### Problems

- Nmap service fingerprinting of open ports is slow and can change the observed state of `25/tcp`, `110/tcp`, and `143/tcp`.
- `ffprobe` and `ffmpeg` are still not available in PATH.
- `8800/tcp` and `9800/tcp` protocol semantics remain unknown.

### Next Step

- Continue to P2-02: test common RTSP URLs, with low expected success because standard RTSP ports are closed.

---

## Experiment ID: EXP-0014

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P2-02 |
| Goal | Test common RTSP stream URLs |
| Device State | Camera online on Windows Mobile Hotspot |
| Network State | Camera reachable at 192.168.137.177 |
| Tools Used | nmap / curl.exe / manual TCP RTSP probe |
| Related Files | 03_video_stream_test/rtsp_tests/rtsp_test_results.md / 03_video_stream_test/rtsp_tests/20260514_p2_02_rtsp_ports.txt |

### Steps

1. Checked local availability of `ffprobe`, `ffmpeg`, and `curl.exe`.
2. Confirmed `ffprobe` and `ffmpeg` were not available in PATH.
3. Confirmed this Windows `curl.exe` build has RTSP disabled.
4. Scanned common RTSP/video-related TCP ports.
5. Considered common RTSP URL patterns on `554/tcp`, `8554/tcp`, and `10554/tcp`.
6. Sent manual RTSP `OPTIONS` and `DESCRIBE` requests to `8800/tcp` and `9800/tcp`.
7. Recorded results in `03_video_stream_test/`.

### Observations

- `554/tcp`, `8554/tcp`, and `10554/tcp` are closed.
- Other common streaming-related ports checked in this step, including `1554/tcp`, `1935/tcp`, `7070/tcp`, `8000/tcp`, and `8080/tcp`, are closed.
- `8800/tcp` and `9800/tcp` remain open.
- Manual RTSP `OPTIONS` and `DESCRIBE` requests to `8800/tcp` produced no response.
- Manual RTSP `OPTIONS` and `DESCRIBE` requests to `9800/tcp` produced no response.

### Results

- P2-02 is complete.
- No local RTSP stream was found.
- Common RTSP URL patterns are not viable because the standard RTSP ports are closed.
- `8800/tcp` and `9800/tcp` do not behave like normal RTSP services.

### Problems

- `ffprobe` and `ffmpeg` are not available in PATH.
- `curl.exe` cannot directly test RTSP URLs because RTSP support is disabled in this build.

### Next Step

- Continue to P2-03 ONVIF testing for completeness, with low expected success because `3702/udp` is closed.

---

## Experiment ID: EXP-0015

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P2-03 |
| Goal | Test whether the camera exposes ONVIF / WS-Discovery |
| Device State | Camera online on Windows Mobile Hotspot |
| Network State | Camera reachable at 192.168.137.177 |
| Tools Used | nmap / PowerShell UDP WS-Discovery probe |
| Related Files | 03_video_stream_test/onvif_tests/onvif_test_results.md |

### Steps

1. Scanned common UDP discovery ports, including `3702/udp`.
2. Scanned common ONVIF HTTP/TCP service ports.
3. Sent a manual SOAP WS-Discovery Probe to multicast `239.255.255.250:3702`.
4. Sent the same manual WS-Discovery Probe directly to `192.168.137.177:3702`.
5. Listened for WS-Discovery responses.
6. Recorded results in `03_video_stream_test/onvif_tests/`.

### Observations

- `3702/udp` is closed.
- `1900/udp`, `5353/udp`, `8899/udp`, `5000/udp`, `5001/udp`, `8080/udp`, and `80/udp` are closed.
- Common ONVIF HTTP/TCP ports, including `80/tcp`, `8080/tcp`, `8899/tcp`, `5000/tcp`, `5001/tcp`, `8000/tcp`, `8001/tcp`, `8081/tcp`, `8088/tcp`, and `8090/tcp`, are closed.
- Manual WS-Discovery Probe sent to `239.255.255.250:3702` received no response.
- Manual WS-Discovery Probe sent to `192.168.137.177:3702` received no response.

### Results

- P2-03 is complete.
- No local ONVIF interface was found.
- The camera does not appear to support standard ONVIF discovery or common ONVIF HTTP service ports in the current network state.

### Problems

- GUI ONVIF Device Manager was not used in this step, but command-line WS-Discovery and port evidence are already sufficient for an initial negative result.

### Next Step

- Continue to P2-04: HTTP/MJPEG and proprietary local service checks, focusing especially on `8800/tcp` and `9800/tcp`.

---

## Experiment ID: EXP-0016

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P2-04 |
| Goal | Test HTTP/MJPEG paths and private local services |
| Device State | Camera online on Windows Mobile Hotspot |
| Network State | Camera reachable at 192.168.137.177 |
| Tools Used | curl.exe / tshark / Wireshark |
| Related Files | 03_video_stream_test/http_stream_tests/http_mjpeg_private_service_results.md / 03_video_stream_test/http_stream_tests/20260514_p2_04_app_preview_private_ports_camera_192.168.137.177.pcapng |

### Steps

1. Tested common HTTP/MJPEG paths on `80/tcp`, `8800/tcp`, and `9800/tcp`.
2. Started a 100-second camera-filtered dynamic capture.
3. Asked the operator to enter preview, press one direction key, exit preview, and enter preview again during the capture.
4. Extracted IP, TCP, UDP, DNS, TLS, and local TCP 8800 evidence from the capture.
5. Compared local private-port traffic against cloud traffic.

### Observations

- `80/tcp` did not provide a usable web/MJPEG response.
- `8800/tcp` accepted TCP connections, but common HTTP/MJPEG paths returned empty reply.
- `9800/tcp` accepted TCP connections, but common HTTP/MJPEG paths returned empty reply or timeout.
- Dynamic capture saved as `20260514_p2_04_app_preview_private_ports_camera_192.168.137.177.pcapng`.
- The capture contained 153 packets over 95.776676100 seconds.
- Two local phone-to-camera `8800/tcp` 16-byte payloads appeared at about 38.60s and 41.87s.
- Payloads observed: `aa000000e803e803ea03e80300000000` and `bc000000000000000000000000000000`.
- No `9800/tcp` traffic appeared in the dynamic App capture.
- Cloud endpoints remained active: `devota.av380.net` / `218.91.170.134:443` and `ipc79.w390.net` / `120.27.12.196`.
- The capture volume was far too small for a local video stream.

### Results

- P2-04 is complete.
- No local HTTP/MJPEG stream was found.
- `8800/tcp` is confirmed as a local private camera service used during App interaction.
- `9800/tcp` is open but was not used during this App preview/control scenario.
- There is still no evidence of a standard local video stream.

### Problems

- The exact manual action timing may be approximate.
- The private `8800/tcp` binary payload semantics are not decoded.
- Camera-filtered capture cannot fully show phone-to-cloud traffic.

### Next Step

- Continue to P2-06 as a decision gate, because P2-05 requires an available stream and no usable local video stream has been found.

---

## Experiment ID: EXP-0017

| Item | Value |
| --- | --- |
| Date | 2026-05-14 |
| Operator | Luessiaw / Codex |
| Stage | P2-06 |
| Goal | Decide whether the camera can be used without firmware or serial work by directly pulling a local stream |
| Device State | Analysis performed from completed P1/P2 evidence |
| Network State | No new network action; decision based on previous captures and scans |
| Tools Used | Existing P1/P2 analysis notes |
| Related Files | 03_video_stream_test/p2_06_no_flash_stream_decision.md |

### Steps

1. Reviewed P1 preview, PTZ, and blocked-internet evidence.
2. Reviewed P2-01 port scan results.
3. Reviewed P2-02 RTSP results.
4. Reviewed P2-03 ONVIF results.
5. Reviewed P2-04 HTTP/MJPEG and private-service results.
6. Determined whether P2-05 has a valid stream input.
7. Wrote the P2-06 decision note.

### Observations

- No standard RTSP stream was found.
- No ONVIF / WS-Discovery interface was found.
- No HTTP/MJPEG stream was found.
- `8800/tcp` is a real local private service and carries small binary payloads during App interaction.
- `9800/tcp` is open but was not used in the P2-04 App scenario.
- No local high-volume video-like flow was observed.
- App preview still correlates with cloud endpoints and fails to reconnect when public internet is unavailable.

### Results

- P2-06 is complete.
- Current decision: no usable local video stream is available.
- P2-05 is blocked because there is no stream whose codec, resolution, frame rate, or bitrate can be measured.
- The project should not proceed directly to server-side stream ingestion yet.

### Problems

- `8800/tcp` and `9800/tcp` protocol semantics remain unknown.
- Cloud protocol emulation remains theoretically possible but likely high-complexity.

### Next Step

- Proceed to P3 read-only UART investigation before any firmware backup or firmware modification.
