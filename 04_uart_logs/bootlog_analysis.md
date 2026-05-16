# Bootlog Analysis

Source log:

```text
04_uart_logs/raw_logs/20260516-2023MobaXterm terminal output.log
```

Date analyzed: 2026-05-16

## UART Settings

| Item | Value |
| --- | --- |
| Baud Rate | 115200 |
| Data Bits | 8 |
| Parity | None |
| Stop Bits | 1 |
| Flow Control | None |
| Wiring | Camera GND -> USB-TTL GND; Camera TX -> USB-TTL RXD |
| USB-TTL level | 3.3 V after correction |

Notes:

- The first part of the log contains garbled data and MobaXterm session restart text, likely from contact instability or an interrupted session.
- After the wiring/level correction, the log contains readable U-Boot, Linux kernel, and application startup output.
- The USB-TTL module was initially set to 5 V; after switching to 3.3 V, the board speaker noise stopped. Continue using 3.3 V only.

## Boot Information

| Item | Value |
| --- | --- |
| Bootloader | U-Boot `2019.10.0-V4.0.15-g9dd3ddaf` |
| Bootloader build | 2024-02-20 11:32:24 +0800 |
| Abort boot | Disabled (`disable abortboot...`) |
| Kernel Version | Linux `4.4.282` |
| Kernel build | 2024-04-07 15:51:45 CST |
| Toolchain | Buildroot `2018.02.7_V1.0.04-g78fae67`, GCC 5.5.0 |
| SoC | Anyka `AK3918EV300L` |
| Board model | `EVB_CBDM_AK3918EV300L_V1.0.0` / U-Boot model `EVB_CBD_AK3918EV300L_V1.0.0` |
| CPU clock | 888 MHz |
| DDR | 64 MiB |
| Console | `ttySAK0,115200n8` |
| RootFS | `/dev/mtdblock5`, SquashFS, read-only |
| Login prompt | Present: `GZhongshi login:` |
| Shell access | Not tested. Do not type yet during read-only phase. |

## Flash and Partition Map

Detected SPI flash:

```text
XM25QH128C, 16 MiB, page 256 B, erase 4 KiB
```

Kernel command line partition map:

| Name | Offset | End | Size |
| --- | ---: | ---: | ---: |
| UBOOT | `0x000000` | `0x037000` | 220 KiB |
| ENV | `0x037000` | `0x038000` | 4 KiB |
| ENVBK | `0x038000` | `0x039000` | 4 KiB |
| DTB | `0x039000` | `0x049000` | 64 KiB |
| KERNEL | `0x049000` | `0x23d000` | 2000 KiB |
| ROOTFS | `0x23d000` | `0x431000` | 2000 KiB |
| SND | `0x431000` | `0x5be000` | 1588 KiB |
| EXT | `0x5be000` | `0x6b8000` | 1000 KiB |
| JFFS2 | `0x6b8000` | `0x767000` | 700 KiB |
| BACKUP_EN | `0x767000` | `0x768000` | 4 KiB |
| USR | `0x768000` | `0x9c0000` | 2400 KiB |
| USR2 | `0x9c0000` | `0xc18000` | 2400 KiB |
| MVS | `0xc18000` | `0xe0c000` | 2000 KiB |
| MVS2 | `0xe0c000` | `0x1000000` | 2000 KiB |
| ALL | `0x000000` | `0x1000000` | 16 MiB |

Mounted filesystems observed:

```text
VFS: Mounted root (squashfs filesystem) readonly on device 31:5.
mount /dev/mtdblock10 for usr
mount /dev/mtdblock12 for mvs
```

Useful implication:

- P4 flash backup should target the full 16 MiB SPI NOR.
- The partition map is now known and should be reused when analyzing dumps.
- `USR`, `USR2`, `MVS`, and `MVS2` are likely important application/config partitions.

## Hardware and Driver Findings

| Component | Evidence |
| --- | --- |
| Image sensor | `sc2336` probed successfully |
| Sensor resolution | 1920x1080 |
| Video subsystem | Linux media interface and video capture interface initialized |
| Encoder | `ak_venc_*` logs and `mvp_video_venc_init` observed |
| Audio | `mv_ao_init`, `mv_ai_init`, MP3 prompt playback observed |
| PTZ motor | `ak_motor_probe`, `ptz ctrl init`, PTZ position and movement logs observed |
| WiFi | AltoBeam / ATBM `6012B` USB WiFi, `atbm603x_wifi_usb.ko` |
| MAC | `58:c5:87:9a:ab:97` |
| SD card | `/dev/mmcblk0p1` mounted at `/mnt/sdcard`; recording files observed |

Sensor and media details:

```text
sc2336 Probed success
sensor width:1920 high:1080
mvp_isp_init
mvp_video_venc_init
ak_venc_request_idr [0] success
media init finish
```

This confirms that the device has an active local capture/encoding pipeline even though no standard LAN stream was exposed in P2.

## Startup Scripts and Config Paths

Important paths seen in the log:

| Path / File | Evidence |
| --- | --- |
| `/mnt/mtd/nvipcstart.sh` | Startup script; reports missing `/mnt/mtd/try_prerun.sh` |
| `/mnt/mtd/mvconf/default/factory_cfg.ini` | Factory config read and MD5 checked |
| `/mnt/mtd/mvconf/avframe_attr.ini` | Video/audio frame config read |
| `/mnt/mtd/mvconf/record.ini` | Recording config read |
| `/mnt/mtd/mvconf/factory_const.ini` | Factory constants read |
| `/mnt/mtd/mvconf/user_info.ini` | User info config read |
| `/mnt/mtd/mvconf/version.ini` | Version config read |
| `/mnt/mtd/mvsound/*.mp3` | Chinese voice prompts |
| `/mvs/apps/udhcpc/dns_proxy` | DNS proxy binary/path printed |

Version line:

```text
version:V1.1.0 build date:Aug 19 2024 09:55:19
```

Pre-run line:

```text
[PRERUN] build:Feb 18 2024_12:15:54 version:V1.0.0
```

## Network and Cloud Findings

WiFi startup:

```text
[WIFI] mac:58:c5:87:9a:ab:97
udhcpc -i wlan0 -r 192.168.137.177
configRspID: 0 restart ip:192.168.137.177 mac:58:c5:87:9a:ab:97 netmask:255.255.255.0 gw:192.168.137.1
```

Cloud/P2P:

```text
platform_cloud_service_init start
mv_main_handel_ota_init start
new main P2P Domain: ipc79.w390.net => [120.27.12.196]
Logon success! Using P2P Svr [0]
```

OTA/TLS:

```text
[mvt_ota] [TLS]Handshake failed -16[-0x0010]
[mvt_ota] [TCP]Connect [218.91.199.250:443] failed
[mvt_ota] [TCP]Connect [58.221.37.119:443] failed
[mvt_ota] [TCP]Connect [58.221.36.18:443] failed
```

These UART logs strongly confirm the earlier network-capture conclusions:

- `ipc79.w390.net` / `120.27.12.196` is the main P2P/cloud endpoint.
- `devota.av380.net`-related 443 endpoints likely include OTA/cloud service behavior.
- Cloud login succeeds after WiFi and DHCP.

## RTSP / Local Stream Clues

The boot log contains RTSP-related function names:

```text
f:mvs_rtsp_restart l:378
f:mvs_rtsp_restart l:381
=== rtsp exit ===
=== rtsp exit end ===
```

Interpretation:

- RTSP-related code appears to exist in the application stack.
- The runtime log shows RTSP restart/exit behavior, but P2 found no open RTSP port.
- This may mean RTSP is compiled in but disabled, exits when cloud/P2P mode is active, requires config, or binds only under specific conditions.
- This is one of the most important leads for firmware/config analysis.

## PTZ Findings

PTZ initialization:

```text
ptz ctrl init
ptz init finish
```

Observed movement logs:

```text
ptz turn to left: [step:175]
ptz turn to right: [step:175]
ptz turn to up: [step:187]
ptz turn to down: [step:187]
mvp ptz pos [horizon:251] [vertical:2]
```

Implication:

- UART logs can directly reveal PTZ commands and current position.
- This will help later map App actions and local `8800/tcp` payloads to PTZ behavior.

## 8800 / 9800 Port Attribution

The current boot log does not directly print `8800` or `9800`.

Potentially related service logs:

```text
mv_server_init init start
mv_server_init init finish
login handle create
mvs_dd_service_init start
```

Interpretation:

- `8800/tcp` may be part of `mv_server` or another MVS service, but the log does not prove port ownership.
- `9800/tcp` ownership is still unknown.
- P3-09 is not complete yet; it requires either more verbose logs, interactive read-only-safe commands after approval, or firmware/rootfs analysis.

## Dynamic App Operation UART Capture

Additional source log:

```text
04_uart_logs/raw_logs/20260516-2038.log
```

Scenario:

1. Power on.
2. Wait for network connection success.
3. Open preview in the phone App.
4. Tap "HD" / high-definition mode.
5. Press left, right, up, and down PTZ buttons.
6. Exit preview.
7. Power off.

### Dynamic Capture Quality

This second log is cleaner than the first one. It starts from U-Boot and captures a readable Linux/application startup sequence.

It confirms the same base platform:

| Item | Value |
| --- | --- |
| U-Boot | `2019.10.0-V4.0.15-g9dd3ddaf` |
| Kernel | Linux `4.4.282` |
| SoC | `AK3918EV300L` |
| Flash | `XM25QH128C`, 16 MiB |
| App version | `V1.1.0`, build date 2024-08-19 09:55:19 |

### Network and Cloud Events

The second log again confirms the cloud/P2P sequence:

```text
platform_cloud_service_init start
mv_main_handel_ota_init start
f:mvs_rtsp_restart l:378
new main P2P Domain: ipc79.w390.net => [120.27.12.196]
Logon success! Using P2P Svr [0]
```

The log also shows a DDNS/P2P-style domain:

```text
<device-id>.nvdvr.net
```

The exact numeric device ID and credentials are intentionally not copied into this analysis file.

### Preview / HD Clues

Around the App preview / HD interaction window, the following events appear:

```text
login handle create
vchn:1, level_cc:100
ak_venc_request_idr [1] success
cmd:327
new version: [69][]
talk recv size[0/16] < header again exit break
vchn:1, level_cc:103
vchn:0, level_cc:100
ak_venc_request_idr [0] success
vchn:0, level_cc:101
```

Interpretation:

- App preview and/or quality switching causes encoder IDR requests.
- `vchn:0` and `vchn:1` likely refer to video channels or stream profiles.
- The "HD" click likely correlates with `vchn` / `level_cc` changes and IDR refreshes, but the exact mapping is not proven yet.
- `talk recv size[0/16]` appears during the App session. This is probably an App session/talk/control channel event, not proof of audio talk use.

Important:

- These UART events confirm that local encoding is active.
- They still do not prove a local LAN video stream exists.
- They fit the P2 finding that the App/cloud session requests encoded frames through the vendor stack.

### PTZ Operation Mapping

The App PTZ actions are clearly visible:

| App Action | UART Evidence | Position Result |
| --- | --- | --- |
| Left | `ptz turn to left: [step:175]` repeated | `mvp ptz pos [horizon:288] [vertical:2]` |
| Right | `ptz turn to right: [step:175]` repeated | `mvp ptz pos [horizon:245] [vertical:2]` |
| Up | `ptz turn to up: [step:187]` repeated | `mvp ptz pos [horizon:245] [vertical:44]` |
| Down | `ptz turn to down: [step:187]` repeated | `mvp ptz pos [horizon:245] [vertical:2]` |

Additional PTZ settings observed:

```text
switch ptz speed hz : 500
set motor h speed :500
set motor v speed : 500
need to record cur postion h:245 v:2
```

Interpretation:

- UART logs can reliably identify PTZ commands and resulting positions.
- The App direction buttons are handled inside the firmware/application stack, not only in cloud logs.
- This gives a strong future path for mapping `8800/tcp` payloads to PTZ commands if packet capture and UART logging are run at the same time.

### Updated RTSP Interpretation

The second log again shows:

```text
f:mvs_rtsp_restart l:378
=== rtsp exit ===
=== rtsp exit end ===
```

Updated interpretation:

- RTSP-related logic exists and is invoked during network/cloud startup.
- The runtime exits RTSP shortly after cloud/P2P login.
- This strengthens the hypothesis that RTSP support may be compiled in but disabled, not configured, or dependent on a runtime mode.
- Offline firmware/rootfs analysis should search for `mvs_rtsp_restart`, RTSP config keys, and related strings.

### Updated P3-09 Status

P3-09 remains partial.

New evidence:

- `mv_server_init`, `mvs_dd_service_init`, `login handle create`, and App session events are visible.
- App preview/HD triggers encoder/channel events.
- PTZ commands are visible and mappable.

Still missing:

- No direct `8800` or `9800` string appears in the UART log.
- No explicit process-to-port ownership is printed.

Best next evidence source:

- Simultaneous UART + packet capture while pressing one PTZ direction at known timestamps.
- Or, after explicit approval, interactive read-only commands such as `netstat`, `ps`, and `mount`.
- Or P4 firmware backup and offline string/rootfs analysis.

## Important Safety Notes

Do not connect USB-TTL TX to camera RX yet.

Reasons:

- A login prompt exists, but authentication and shell behavior are unknown.
- U-Boot abort is disabled, and interacting with bootloader is not needed now.
- Current project stage is still read-only evidence collection.

If later approved for interactive UART, first action should be minimal and non-destructive, such as pressing Enter at login only after documenting the risk.

## P3 Status

| Task | Status | Notes |
| --- | --- | --- |
| P3-01 | Complete | GND confirmed |
| P3-02 | Complete | 3.3 V TTL confirmed |
| P3-03 | Complete | Read-only wiring confirmed |
| P3-04 | Complete | MobaXterm serial logging used |
| P3-05 | Complete | Boot log observed |
| P3-06 | Not needed | 115200 8N1 works |
| P3-07 | Complete | Raw boot log saved |
| P3-08 | Complete for initial pass | System, partition, service, media, WiFi, cloud findings extracted |
| P3-09 | Partial | `8800/9800` ownership not directly printed |

## Recommended Next Step

Proceed to P3-09 follow-up planning:

1. Preserve this raw boot log unchanged.
2. Capture one cleaner boot log if convenient, starting before power-on and avoiding contact movement.
3. Do not connect USB-TTL TX yet.
4. Decide whether to proceed with:
   - another read-only UART capture during App preview/PTZ,
   - approved interactive UART checks,
   - or P4 full SPI flash backup and offline rootfs analysis.

Most useful near-term option:

- Capture UART log while opening App preview and pressing PTZ directions, then correlate `mvs_rtsp_restart`, `mv_server`, `login handle`, PTZ, and cloud/P2P messages with App behavior.
