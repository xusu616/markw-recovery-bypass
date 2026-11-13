# 下载来源

本目录二进制镜像默认不提交到仓库（见 `.gitignore`）。

- `cofface_twrp_recovery_markw_1121.img`：适用于 Redmi 4 Prime（`markw`）Android 6.0.1 / MIUI 8 的 Cofface TWRP。
- `cofface_twrp_recovery_markw_1121-appended.img`：使用 `scripts/append-boot-footer.py` 为上述镜像追加 4096 字节尾块后的实测可用版本。
- `twrp-3.4.0-1-markw.img`：来自 `redispade/device_xiaomi_markw_twrp` 发布页（仅适用于 Android 9/10，在 MIUI 8 Android 6.0.1 环境下无法直接引导）。
- `twrp_3.7.0_12-1-markw_by_SonicBSV_18_11_2023.img`：来自 AndroidFileHost SonicBSV 目录（`https://androidfilehost.com/?fid=16385555061192795609`），用于 Android 11~14 Treble ROM。
- `twrp_3.7.0_12-1-markw_by_SonicBSV_18_11_2023-appended.img`：追加 4096 字节尾块后的实测可用版本，已配合 `crDroidAndroid-14.0-20240803-markw-v10.6.zip` 验证启动。
