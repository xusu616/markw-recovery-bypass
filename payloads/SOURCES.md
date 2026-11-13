镜像及配置在本地已备齐。仓库默认保存脚本、XML、小体积签名引导与校验值。

来源、生成方法、实测状态和文件哈希见根目录 `README.md` 与 `SHA256SUMS.txt`。

- `emmc_appsboot-miui8-v8050-original.mbn`：取自官方国行稳定版 `MIUI V8.0.5.0.MBECNDG`（`markw_images_V8.0.5.0.MBECNDG_20160805.0000.29_6.0_cn_ad9f9a6c19.tgz`）。
- `aboot-miui8-v8050-signed-1MiB.bin`：仅在原始小米签名 MBN 尾部补零至 `1,048,576` 字节（1 MiB），未修改任何代码或签名。
- `misc-boot-recovery-512B.bin`：512 字节 `misc` 分区触发镜像，开头为 `boot-recovery\0`，其余补零。
- `rawprogram_markw_*.xml`：对应 Redmi 4 Prime（`markw` / MSM8953）GPT 分区表 512 字节扇区偏移的 Firehose 烧录描述文件。
