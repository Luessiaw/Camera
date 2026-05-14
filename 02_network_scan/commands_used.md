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

## ffmpeg / ffprobe

```bash
ffprobe rtsp://<camera_ip>:554/<path>
ffmpeg -i rtsp://<camera_ip>:554/<path> -f null -
```
