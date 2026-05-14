# Commands Used

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

## P2-01 Commands

```powershell
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p- --min-rate 1000 -oN '02_network_scan\nmap\20260514_p2_01_tcp_all_ports.txt' -oX '02_network_scan\nmap\20260514_p2_01_tcp_all_ports.xml' 192.168.137.177
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sU -Pn -n --reason --top-ports 100 -oN '02_network_scan\nmap\20260514_p2_01_udp_top100.txt' -oX '02_network_scan\nmap\20260514_p2_01_udp_top100.xml' 192.168.137.177
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sV -Pn -n --version-intensity 2 --reason -p 25,110,143,8800,9800 -oN '02_network_scan\nmap\20260514_p2_01_open_ports_service_light.txt' -oX '02_network_scan\nmap\20260514_p2_01_open_ports_service_light.xml' 192.168.137.177
& 'C:\Program Files (x86)\Nmap\nmap.exe' -sT -Pn -n --reason -p 25,110,143,8800,9800 -oN '02_network_scan\nmap\20260514_p2_01_tcp_open_ports_rescan.txt' -oX '02_network_scan\nmap\20260514_p2_01_tcp_open_ports_rescan.xml' 192.168.137.177
```

## ffmpeg / ffprobe

```bash
ffprobe rtsp://<camera_ip>:554/<path>
ffmpeg -i rtsp://<camera_ip>:554/<path> -f null -
```
