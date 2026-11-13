# Redmi 4 Prime（`markw`）ROM 选型记录

> 当前状态（2026-11-13）：已完成 `MIUI V8.0.5.0.MBECNDG` `aboot` + `cofface_twrp_recovery_markw_1121-appended.img` 刷入并成功进入 TWRP（ADB root 正常，`/data` 可用 `22.4 GiB`，`misc` 已清零）。尚未刷入新 ROM。

## 一、Non-Treble 与 Treble 分区差异

红米 4 高配版（`markw` / Snapdragon 625）出厂为 Android 6.0.1，原厂分区表没有独立 `vendor` 分区：

1. **Non-Treble ROM（可用当前 Cofface TWRP 直接刷入）**：
   - 包括 Xiaomi.eu MIUI 10.2（Android 6.0）、LineageOS 14.1（Android 7.1.2）、Resurrection Remix v5.7.4/v5.8.5。
   - 不需要改用 Treble 分区方案，直接配合当前 `cofface_twrp_recovery_markw_1121-appended.img` 刷入即可。
2. **Treble ROM（Android 9 ~ 14，需先更换对应 Treble TWRP）**：
   - 社区将 `cust` 分区映射为 `/vendor` 以支持 Project Treble。
   - Android 9 / 10 需搭配 `twrp-3.4.0-1-markw`（已补尾块版 `roms/twrp-3.4.0-1-markw-appended.img`）；Android 11 ~ 14（如 SonicBSV 构建）需搭配 `twrp_3.7.0_12-1-markw_by_SonicBSV.img` 并用 `scripts/append-boot-footer.py` 追加尾块。

> **关键规则**：无论选择哪种 ROM，刷完 ZIP 后（以及后续使用 Magisk 修补 `boot.img` 后），**必须在重启前从安装包提取 `boot.img`，运行 `scripts/append-boot-footer.py` 追加 4096 字节尾块并写回 `boot` 分区**。

---

## 二、候选 ROM 清单（待实测选择）

### 1. Non-Treble 候选（最稳妥，当前 TWRP 直刷）

- **Xiaomi.eu MIUI 10.2 Stable（Android 6.0.1）**
  - 文件参考：`xiaomi.eu_multi_HM4Pro_V10.2.1.0.MBECNXM_v10-6.0.zip`
  - 来源：[SourceForge Xiaomi.eu Stable](https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/) / [AndroidFileHost](https://www.androidfilehost.com/?w=files&flid=288009)
  - 特点：贴近原厂、功耗低、相机与指纹（FPC/Goodix）兼容性最好。
- **LineageOS 14.1（Android 7.1.2）**
  - 文件参考：`lineage-14.1-20171020-UNOFFICIAL-markw.zip`
  - 来源：[AndroidFileHost brigudav markw 目录](https://www.androidfilehost.com/?w=files&flid=202353)
  - 特点：纯净轻量，VoLTE 正常，部分 Goodix 指纹批次可能需额外补丁。

### 2. Treble 候选（较高 Android 版本，需先换支持 Treble 的带尾块 TWRP）

- **LineageOS 17.1 / 18.1 / 19.1（Android 10 / 11 / 12L，SonicBSV 维护）**
  - 来源：[AndroidFileHost SonicBSV 目录 (flid=330752)](https://www.androidfilehost.com/?w=files&flid=330752)
  - 配套 Recovery：`twrp_3.7.0_12-1-markw_by_SonicBSV.img`（同目录，需先追加 4096 字节尾块）
- **crDroid v6.12（Android 10）/ v9.11（Android 13）/ v10.6（Android 14）**
  - Android 10 来源：[SourceForge crdroid-markw](https://sourceforge.net/projects/crdroid-markw/files/)（需 TWRP 3.4.0-1）
  - Android 13/14 来源：[AndroidFileHost SonicBSV 目录 (flid=330752)](https://www.androidfilehost.com/?w=files&flid=330752)（需 SonicBSV TWRP 3.7.0）
- **Pixel Experience Plus 9.0（Android 9.0）**
  - 来源：[SourceForge Pixel Experience Plus markw](https://sourceforge.net/projects/pixel-experience-plus-edition-markw/files/)
- **Havoc-OS v3.0（Android 10）**
  - 来源：[SourceForge Havoc-OS markw](https://sourceforge.net/projects/havoc-os/files/markw/)
