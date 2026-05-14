# Command Cheatsheet

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
