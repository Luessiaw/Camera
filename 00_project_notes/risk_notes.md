# Risk Notes

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
