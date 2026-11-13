# Markw Bootloader & Recovery 诊断记录（2026-11-12 ~ 2026-11-13）

## 设备与初始状态

- 机型：Xiaomi Redmi 4 Prime（`markw` / Snapdragon 625 / MSM8953）
- 原机系统：MIUI 8（`V8.2.1.0` 系列内核与 `aboot`）
- 原机引导状态：锁定 bootloader（`androidboot.verifiedbootstate=green`，`androidboot.veritymode=enforcing`）
- 原始备份保存在 `local-only/markw-diagnosis-20261112/`（不纳入 Git 追踪）：
  - `gpt-primary.bin`
  - `aboot.bin`、`abootbak.bin`
  - `devinfo.bin`
  - `recovery-original.bin`

## 关键发现

1. **高版本 MIUI `aboot` 与旧版 `V8.0.5.0` `aboot` 的行为差异**
   - 随设备原带的 `V8.2.1.0` `aboot` 在遇到追加 4096 字节尾块（`30 83 19 89 64` + 零填充）的自定义镜像时无法启动，进入 900E。
   - 改用官方国行稳定版 `MIUI V8.0.5.0.MBECNDG` 提取的原始签名 `emmc_appsboot.mbn`（尾部补零对齐至 `1,048,576` 字节，未修改任何代码或签名），同时写入 `aboot`（LBA `786432`）和 `abootbak`（LBA `788480`）后，实测可正常引导追加尾块的镜像。

2. **`twrp-3.4.0-1-markw` 与 MIUI 8 不兼容**
   - `redispade/device_xiaomi_markw_twrp` 发布的 `twrp-3.4.0-1-markw.img` 仅适配 Android 9 / 10（`Pie and Q`），在当前 Android 6.0.1（MIUI 8）环境无法进入恢复界面。
   - 改用 Android 6.0.1 原配 `cofface_twrp_recovery_markw_1121.img` 并用 `scripts/append-boot-footer.py` 追加 4096 字节尾块（生成 `cofface_twrp_recovery_markw_1121-appended.img`）后，已成功匹配当前环境。

3. **`adb reboot recovery` 失效原因与 `misc` 分区方案**
   - `V8.0.5.0` `aboot` 读取重启标志的方式与较新 `V8.2.1.0` 内核写入的位置不一致，导致执行 `adb reboot recovery` / `adb reboot bootloader` 时直接重启进入 Android 系统；且 MIUI 开机脚本会将 `recovery` 还原为官方版本。
   - 静态分析 `V8.0.5.0` `aboot` 的 `emmc_recovery_init` 逻辑确认：只要 `misc` 分区（LBA `8060928`）开头写入 `boot-recovery\0`，开机时无论按键和 USB 状态如何都会直接进入 `recovery`。
   - 2026-11-13 实测：使用 `scripts/flash_markw_miui8_aboot_and_twrp.py` 在单个 Firehose 会话中连续写入 `aboot`、`abootbak`、`recovery` 与 `misc-boot-recovery-512B.bin` 后，拔掉 USB 并按电源键直接进入 Cofface TWRP；TWRP 启动后已自动将 `misc` 清零，`adb`（root）与 `/data`（`dm-0`，可用 `22.4 GiB`）均工作正常。
