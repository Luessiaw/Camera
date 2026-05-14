# Rollback Plan

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
