# GitHub Actions 自动发布 Release 指南

## 概述

项目已配置 GitHub Actions，可以在发布 Release 时自动编译 Windows、macOS、Linux 的可执行文件。

## 🎯 工作流程

### 自动触发方式（推荐）

当你推送一个版本标签时，会自动触发构建和发布：

```bash
# 1. 确保所有改动已提交
git add -A
git commit -m "feat: 发布 v8.6.0 版本"

# 2. 创建版本标签
git tag v8.6.0

# 3. 推送代码和标签
git push origin main
git push origin v8.6.0
```

**自动执行的操作：**
1. ✅ 在 Windows、macOS (Intel)、macOS (ARM)、Linux 上构建
2. ✅ 打包成可执行文件
3. ✅ 创建 GitHub Release
4. ✅ 上传所有构建产物到 Release

### 手动触发方式

如果需要手动触发构建：

1. 进入 GitHub 仓库页面
2. 点击 `Actions` 标签
3. 选择 `Build and Release` workflow
4. 点击右侧 `Run workflow` 按钮
5. 输入版本号（如 `v8.6.0`）
6. 点击 `Run workflow`

## 📦 发布产物

每次发布会生成以下文件：

| 文件名 | 平台 | 说明 |
|--------|------|------|
| `LinuxDoHelper_Windows.exe` | Windows | 直接双击运行 |
| `LinuxDoHelper_macOS_Intel.zip` | macOS Intel | 解压后运行 |
| `LinuxDoHelper_macOS_ARM.zip` | macOS Apple Silicon | 解压后运行 |
| `LinuxDoHelper_Linux.tar.gz` | Linux | 解压后在终端运行 |

## 📝 完整发布流程

### 方法 1：命令行发布（推荐）

```bash
# 1. 确认当前版本号
echo "当前准备发布: v8.6.0"

# 2. 更新版本号（如果还没更新）
# 编辑 linux_do_gui.py 中的 VERSION = "8.6.0"

# 3. 提交所有改动
git add -A
git commit -m "feat: 发布 v8.6.0 版本

- 新增随机间断功能
- 快速浏览层数可自定义
- 完善文档和说明"

# 4. 创建标签
git tag -a v8.6.0 -m "Release v8.6.0

新功能：
- 随机间断功能
- 快速浏览层数自定义

详细内容请查看 CHANGELOG_v8.6.md"

# 5. 推送到 GitHub
git push origin main
git push origin v8.6.0

# 6. 等待 GitHub Actions 自动构建和发布（约 10-15 分钟）
```

### 方法 2：GitHub 网页发布

1. **提交代码**
   ```bash
   git add -A
   git commit -m "feat: 发布 v8.6.0 版本"
   git push origin main
   ```

2. **创建 Release**
   - 进入 GitHub 仓库页面
   - 点击右侧 `Releases` → `Create a new release`
   - `Choose a tag` → 输入 `v8.6.0` → `Create new tag`
   - `Release title`：输入 `v8.6.0`
   - `Describe this release`：输入更新说明
   - 点击 `Publish release`

3. **手动触发构建**
   - 进入 `Actions` 标签
   - 选择 `Build and Release`
   - `Run workflow` → 输入 `v8.6.0`
   - 等待构建完成后，文件会自动上传到 Release

## 🔍 监控构建进度

1. 推送标签后，进入 GitHub 仓库的 `Actions` 标签
2. 查看最新的 `Build and Release` workflow
3. 可以看到 4 个并行任务：
   - Build Windows
   - Build macOS-Intel
   - Build macOS-ARM
   - Build Linux
4. 等待所有任务完成（绿色勾号）
5. 最后会执行 `Create Release` 任务
6. 完成后，在 `Releases` 页面就能看到新发布的版本

## 🎛️ Workflow 配置说明

### 触发条件

```yaml
on:
  push:
    tags:
      - 'v*'  # 推送 v 开头的标签时触发
  workflow_dispatch:  # 允许手动触发
```

### 构建平台

| 平台 | 操作系统 | 说明 |
|------|----------|------|
| Windows | `windows-latest` | Windows 10/11 |
| macOS Intel | `macos-13` | Intel 芯片的 Mac |
| macOS ARM | `macos-latest` | Apple Silicon (M1/M2) |
| Linux | `ubuntu-latest` | Ubuntu 22.04 |

### 构建工具

- Python 3.11
- PyInstaller（自动安装）
- 项目依赖（从 requirements.txt）

## 🐛 常见问题

### Q1: 推送标签后没有触发构建？

**检查：**
1. 标签格式是否正确（必须是 `v` 开头，如 `v8.6.0`）
2. 是否推送了标签：`git push origin v8.6.0`
3. 检查 Actions 是否启用：`Settings` → `Actions` → `General`

### Q2: 构建失败？

**查看日志：**
1. 进入 `Actions` → 点击失败的 workflow
2. 点击失败的任务查看详细日志
3. 常见原因：
   - 依赖安装失败 → 检查 `requirements.txt`
   - 语法错误 → 先本地测试 `python3 -m py_compile linux_do_gui.py`
   - 缺少文件 → 确保 `icon.ico` 存在

### Q3: Release 创建了但没有文件？

**检查：**
1. 确保所有构建任务都成功（绿色勾号）
2. 查看 `Create Release` 任务的日志
3. 检查是否有权限问题：`Settings` → `Actions` → `General` → `Workflow permissions` → 选择 `Read and write permissions`

### Q4: macOS 用户打不开应用？

**解决方法：**
```bash
# macOS 首次运行需要：
# 1. 右键点击应用
# 2. 选择"打开"
# 3. 点击"打开"确认

# 或者使用命令行：
xattr -cr LinuxDoHelper_macOS_ARM.app
```

### Q5: 如何删除错误的 Release？

1. 进入 `Releases` 页面
2. 点击要删除的 Release
3. 点击右上角 `Delete`
4. 删除对应的 Git 标签：
   ```bash
   git tag -d v8.6.0                    # 删除本地标签
   git push --delete origin v8.6.0      # 删除远程标签
   ```

## 📊 构建时间

预计构建时间（参考）：

| 平台 | 时间 |
|------|------|
| Windows | ~5 分钟 |
| macOS Intel | ~8 分钟 |
| macOS ARM | ~8 分钟 |
| Linux | ~4 分钟 |
| **总计** | **~10-15 分钟** |

## 🔐 权限配置

确保 GitHub Actions 有正确的权限：

1. 进入仓库 `Settings`
2. 左侧菜单 `Actions` → `General`
3. 找到 `Workflow permissions`
4. 选择 `Read and write permissions`
5. 勾选 `Allow GitHub Actions to create and approve pull requests`
6. 点击 `Save`

## 📝 Release 描述模板

建议在创建 Release 时使用以下模板：

```markdown
## 🎉 v8.6.0 更新内容

### ✨ 新功能

- 💤 随机间断功能：运行过程中随机暂停休息，模拟真人使用习惯
- 🔧 快速浏览层数可自定义：原固定 3-5 层，现可自由设置

### 📦 下载说明

- **Windows 用户**：下载 `LinuxDoHelper_Windows.exe`
- **macOS 用户（Intel）**：下载 `LinuxDoHelper_macOS_Intel.zip`
- **macOS 用户（Apple Silicon）**：下载 `LinuxDoHelper_macOS_ARM.zip`
- **Linux 用户**：下载 `LinuxDoHelper_Linux.tar.gz`

### 📖 文档

- [功能详细说明](https://github.com/你的用户名/linuxdosss/blob/main/BREAK_FEATURE.md)
- [更新日志](https://github.com/你的用户名/linuxdosss/blob/main/CHANGELOG_v8.6.md)

### 🔗 相关链接

- [使用教程](https://github.com/你的用户名/linuxdosss#使用方法)
- [问题反馈](https://github.com/你的用户名/linuxdosss/issues)
```

## 🚀 快速命令

### 发布新版本（一键脚本）

创建一个 `release.sh` 脚本：

```bash
#!/bin/bash
# 快速发布脚本

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "用法: ./release.sh v8.6.0"
    exit 1
fi

echo "准备发布版本: $VERSION"

# 1. 检查是否有未提交的改动
if [[ -n $(git status -s) ]]; then
    echo "检测到未提交的改动，请先提交"
    git status -s
    exit 1
fi

# 2. 创建标签
git tag -a $VERSION -m "Release $VERSION"

# 3. 推送
git push origin main
git push origin $VERSION

echo "✓ 标签已推送，GitHub Actions 将自动构建和发布"
echo "查看进度：https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
```

使用：
```bash
chmod +x release.sh
./release.sh v8.6.0
```

## ✅ 发布检查清单

发布前请确认：

- [ ] 更新了 `VERSION` 变量（linux_do_gui.py）
- [ ] 更新了 README.md 版本号
- [ ] 创建了 CHANGELOG 文件
- [ ] 本地测试通过（`python3 linux_do_gui.py`）
- [ ] 语法检查通过（`python3 -m py_compile linux_do_gui.py`）
- [ ] Git 标签格式正确（`v8.6.0`）
- [ ] GitHub Actions 权限已配置
- [ ] 准备好 Release 描述

---

**配置文件**: `.github/workflows/release.yml`  
**说明文档**: 本文件  
**更新时间**: 2026-06-23
