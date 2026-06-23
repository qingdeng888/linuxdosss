# GitHub Actions 自动发布配置完成

## ✅ 配置完成

已成功配置 GitHub Actions，可以自动编译和发布多平台的可执行文件。

---

## 📦 发布平台

发布时会自动构建以下平台：

| 平台 | 文件名 | 说明 |
|------|--------|------|
| Windows | `LinuxDoHelper_Windows.exe` | 直接运行 |
| macOS Intel | `LinuxDoHelper_macOS_Intel.zip` | Intel 芯片 Mac |
| macOS ARM | `LinuxDoHelper_macOS_ARM.zip` | Apple Silicon (M1/M2) |
| Linux | `LinuxDoHelper_Linux.tar.gz` | Ubuntu/Debian |

---

## 🚀 快速发布

### 方法 1：使用脚本（最简单）

```bash
# 赋予执行权限（首次需要）
chmod +x release.sh

# 发布新版本
./release.sh v8.6.0
```

脚本会自动：
- ✅ 检查版本号格式
- ✅ 检查是否有未提交的改动
- ✅ 检查标签是否已存在
- ✅ 验证代码中的版本号
- ✅ 创建 Git 标签
- ✅ 推送到 GitHub
- ✅ 触发自动构建

### 方法 2：手动命令

```bash
# 1. 创建标签
git tag v8.6.0

# 2. 推送代码和标签
git push origin main
git push origin v8.6.0

# 3. 等待自动构建（10-15分钟）
```

---

## 📂 新增文件

### 1. Workflow 配置
- **文件**: `.github/workflows/release.yml`
- **功能**: 自动构建和发布
- **触发**: 推送 `v*` 标签

### 2. 发布指南
- **文件**: `RELEASE_GUIDE.md`
- **内容**: 详细的发布流程和问题解决

### 3. 发布脚本
- **文件**: `release.sh`
- **功能**: 一键发布新版本

---

## 🔧 配置说明

### Workflow 特性

```yaml
触发条件:
  - 推送 v* 标签（如 v8.6.0）
  - 手动触发（在 Actions 页面）

构建平台:
  - Windows (windows-latest)
  - macOS Intel (macos-13)
  - macOS ARM (macos-latest)
  - Linux (ubuntu-latest)

自动操作:
  1. 安装依赖
  2. 使用 PyInstaller 构建
  3. 打包文件
  4. 创建 Release
  5. 上传所有文件
```

---

## 📝 发布流程

### 完整流程

```
1. 开发完成
   ├─ 更新版本号（linux_do_gui.py）
   ├─ 更新 README.md
   └─ 创建 CHANGELOG

2. 提交代码
   └─ git commit -m "feat: 发布 v8.6.0"

3. 创建标签
   └─ git tag v8.6.0

4. 推送到 GitHub
   ├─ git push origin main
   └─ git push origin v8.6.0

5. 自动构建（10-15分钟）
   ├─ Build Windows
   ├─ Build macOS Intel
   ├─ Build macOS ARM
   └─ Build Linux

6. 自动发布
   └─ 创建 Release 并上传所有文件
```

---

## 🎯 使用示例

### 发布 v8.6.0

```bash
# 使用脚本（推荐）
./release.sh v8.6.0

# 或手动执行
git tag v8.6.0
git push origin main
git push origin v8.6.0
```

### 查看构建进度

1. 访问 GitHub 仓库
2. 点击 `Actions` 标签
3. 查看最新的 `Build and Release` workflow
4. 等待所有任务完成（绿色勾号）

### 查看发布结果

1. 点击 `Releases` 标签
2. 可以看到新发布的 v8.6.0
3. 下载区有 4 个文件（Windows/macOS/Linux）

---

## ⚙️ GitHub 仓库配置

### 必需配置

1. **启用 Actions**
   - `Settings` → `Actions` → `General`
   - `Allow all actions and reusable workflows`

2. **设置权限**
   - `Settings` → `Actions` → `General`
   - `Workflow permissions`:
     - ✅ 选择 `Read and write permissions`
     - ✅ 勾选 `Allow GitHub Actions to create and approve pull requests`
   - 点击 `Save`

3. **验证配置**
   - 推送一个测试标签
   - 查看 Actions 是否触发
   - 检查是否创建 Release

---

## 🐛 常见问题

### Q1: 推送标签后没有触发构建？

**解决方法:**
```bash
# 1. 检查标签格式（必须是 v 开头）
git tag -l

# 2. 确认标签已推送
git ls-remote --tags origin

# 3. 检查 Actions 是否启用
# Settings → Actions → General
```

### Q2: 构建失败？

**查看日志:**
1. 进入 `Actions` 页面
2. 点击失败的 workflow
3. 点击失败的任务查看详细日志

**常见原因:**
- 依赖安装失败 → 检查 `requirements.txt`
- 语法错误 → 先本地测试
- 权限不足 → 检查 Workflow permissions

### Q3: Release 没有文件？

**检查:**
1. 所有构建任务是否成功（绿色勾号）
2. 查看 `Create Release` 任务日志
3. 确认 `Workflow permissions` 设置为 `Read and write`

### Q4: 如何删除错误的 Release？

```bash
# 1. 在 GitHub 网页删除 Release
# Releases → 点击 Release → Delete

# 2. 删除 Git 标签
git tag -d v8.6.0                    # 删除本地
git push --delete origin v8.6.0      # 删除远程

# 3. 重新发布
./release.sh v8.6.0
```

---

## 📊 构建时间

| 阶段 | 时间 |
|------|------|
| Windows 构建 | ~5 分钟 |
| macOS Intel 构建 | ~8 分钟 |
| macOS ARM 构建 | ~8 分钟 |
| Linux 构建 | ~4 分钟 |
| 创建 Release | ~1 分钟 |
| **总计** | **~10-15 分钟** |

---

## 📖 相关文档

- **RELEASE_GUIDE.md** - 详细发布指南
- **release.sh** - 发布脚本
- **.github/workflows/release.yml** - Workflow 配置

---

## ✅ 配置检查清单

发布前请确认：

- [ ] 已创建 `.github/workflows/release.yml`
- [ ] 已创建 `release.sh` 并赋予执行权限
- [ ] 已配置 GitHub Actions 权限
- [ ] 已测试标签推送流程
- [ ] 已验证构建和发布功能

---

## 🎉 配置完成

现在你可以：
1. 使用 `./release.sh v8.6.0` 快速发布
2. 或手动推送标签自动触发
3. GitHub Actions 会自动构建和发布所有平台

**预计 10-15 分钟后，Release 页面就会有所有平台的可执行文件！**

---

**配置时间**: 2026-06-23  
**配置者**: Claude Code  
**版本**: v8.6.0
