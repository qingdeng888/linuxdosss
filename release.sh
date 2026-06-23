#!/bin/bash
# 快速发布脚本
# 用法: ./release.sh v8.6.0

set -e  # 遇到错误立即退出

VERSION=$1

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 显示使用说明
show_usage() {
    cat << EOF
用法: $0 <版本号>

示例:
  $0 v8.6.0     发布 v8.6.0 版本
  $0 v8.6.1     发布 v8.6.1 版本

说明:
  - 版本号必须以 'v' 开头
  - 脚本会自动创建 Git 标签并推送
  - GitHub Actions 会自动构建和发布

EOF
    exit 1
}

# 检查参数
if [ -z "$VERSION" ]; then
    print_error "缺少版本号参数"
    show_usage
fi

# 检查版本号格式
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "版本号格式错误，必须是 vX.Y.Z 格式（如 v8.6.0）"
    exit 1
fi

echo ""
echo "======================================"
echo "  Linux.do 刷帖助手 - 发布脚本"
echo "======================================"
echo ""

print_info "准备发布版本: $VERSION"
echo ""

# 1. 检查是否在 Git 仓库中
if [ ! -d .git ]; then
    print_error "当前目录不是 Git 仓库"
    exit 1
fi

print_success "Git 仓库检查通过"

# 2. 检查是否有未提交的改动
if [[ -n $(git status -s) ]]; then
    print_warning "检测到未提交的改动："
    git status -s
    echo ""
    read -p "是否继续？改动将不会包含在此版本中 (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消发布"
        exit 0
    fi
fi

# 3. 检查标签是否已存在
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    print_error "标签 $VERSION 已存在"
    echo ""
    read -p "是否删除现有标签并重新创建？(y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "删除本地标签..."
        git tag -d $VERSION

        read -p "是否同时删除远程标签？(y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "删除远程标签..."
            git push --delete origin $VERSION 2>/dev/null || print_warning "远程标签不存在或已删除"
        fi
    else
        print_info "已取消发布"
        exit 0
    fi
fi

# 4. 检查版本号是否在代码中更新
print_info "检查版本号..."
CODE_VERSION=$(grep -oP 'VERSION = "\K[^"]+' linux_do_gui.py || echo "未找到")
EXPECTED_VERSION=${VERSION#v}  # 移除 v 前缀

if [ "$CODE_VERSION" != "$EXPECTED_VERSION" ]; then
    print_warning "代码中的版本号 ($CODE_VERSION) 与发布版本 ($EXPECTED_VERSION) 不一致"
    read -p "是否继续？(y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消发布"
        echo ""
        print_info "请先更新 linux_do_gui.py 中的 VERSION 变量："
        echo "  VERSION = \"$EXPECTED_VERSION\""
        exit 0
    fi
else
    print_success "版本号检查通过: $CODE_VERSION"
fi

echo ""
print_info "准备创建标签和发布..."
echo ""

# 5. 显示发布摘要
cat << EOF
发布摘要:
  版本号: $VERSION
  代码版本: $CODE_VERSION
  当前分支: $(git branch --show-current)
  最新提交: $(git log -1 --oneline)

EOF

read -p "确认发布？(y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "已取消发布"
    exit 0
fi

echo ""
print_info "创建标签 $VERSION..."

# 6. 创建标签
git tag -a $VERSION -m "Release $VERSION

新功能请查看 CHANGELOG_${EXPECTED_VERSION}.md"

print_success "标签创建成功"

# 7. 推送到远程
print_info "推送代码到远程仓库..."
git push origin $(git branch --show-current)
print_success "代码推送成功"

print_info "推送标签到远程仓库..."
git push origin $VERSION
print_success "标签推送成功"

echo ""
echo "======================================"
print_success "发布完成！"
echo "======================================"
echo ""

# 获取仓库 URL
REPO_URL=$(git config --get remote.origin.url | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

cat << EOF
接下来：
  1. GitHub Actions 将自动开始构建（约 10-15 分钟）
  2. 构建完成后会自动创建 Release 并上传文件

查看进度:
  Actions: $REPO_URL/actions
  Releases: $REPO_URL/releases

构建产物:
  - LinuxDoHelper_Windows.exe
  - LinuxDoHelper_macOS_Intel.zip
  - LinuxDoHelper_macOS_ARM.zip
  - LinuxDoHelper_Linux.tar.gz

EOF

# 8. 可选：在浏览器中打开 Actions 页面
read -p "是否在浏览器中打开 Actions 页面？(Y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    if command -v xdg-open > /dev/null; then
        xdg-open "$REPO_URL/actions"
    elif command -v open > /dev/null; then
        open "$REPO_URL/actions"
    else
        print_warning "无法自动打开浏览器，请手动访问："
        echo "  $REPO_URL/actions"
    fi
fi

echo ""
print_success "完成！"
