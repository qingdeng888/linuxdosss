#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v8.6 随机间断功能演示脚本
快速演示新功能的工作原理（无需实际运行浏览器）
"""

import time
import random
from datetime import datetime


class BreakFeatureDemo:
    """随机间断功能演示"""

    def __init__(self):
        self.enable_break = True
        self.break_min = 0.1  # 演示用：6秒
        self.break_max = 0.2  # 演示用：12秒
        self.last_break_time = None
        self.next_break_interval = None
        self.cycle = 0

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def schedule_next_break(self):
        """安排下次休息（演示：0.15-0.25分钟 = 9-15秒）"""
        if not self.enable_break:
            return None
        interval = random.uniform(0.15, 0.25)
        self.log(f"💤 已安排下次休息：约 {int(interval * 60)} 秒后")
        return interval

    def should_take_break(self):
        """检查是否应该休息"""
        if not self.enable_break:
            return False

        if self.last_break_time is None:
            self.last_break_time = time.time()
            self.next_break_interval = self.schedule_next_break()
            return False

        elapsed_minutes = (time.time() - self.last_break_time) / 60

        if self.next_break_interval and elapsed_minutes >= self.next_break_interval:
            return True

        return False

    def take_break(self):
        """执行休息"""
        duration = random.uniform(self.break_min, self.break_max)
        duration_seconds = int(duration * 60)

        self.log("=" * 50)
        self.log(f"💤 开始休息 {duration_seconds} 秒（模拟真人行为）")
        self.log("=" * 50)

        start_break = time.time()
        while (time.time() - start_break) < duration_seconds:
            remaining = duration_seconds - int(time.time() - start_break)
            remaining_mins = remaining // 60
            remaining_secs = remaining % 60
            print(f"\r💤 休息中: {remaining_mins}:{remaining_secs:02d}", end="", flush=True)
            time.sleep(1)

        print()  # 换行

        self.log("=" * 50)
        self.log("✨ 休息结束，继续浏览")
        self.log("=" * 50)

        self.last_break_time = time.time()
        self.next_break_interval = self.schedule_next_break()

    def simulate_work(self):
        """模拟工作循环"""
        self.cycle += 1
        self.log(f"🔄 工作循环 #{self.cycle} - 浏览帖子...")
        time.sleep(2)

    def run_demo(self, duration_seconds=60):
        """运行演示"""
        print("\n" + "=" * 60)
        print("🎉 v8.6 随机间断功能演示")
        print("=" * 60)
        print(f"\n📋 配置:")
        print(f"   - 运行时长: {duration_seconds} 秒")
        print(f"   - 休息间隔: {int(self.schedule_next_break() * 60)} 秒左右（随机）")
        print(f"   - 休息时长: {int(self.break_min * 60)}-{int(self.break_max * 60)} 秒（随机）")
        print(f"   - 模拟真人: 每隔一段时间随机休息\n")
        print("=" * 60)
        print("开始演示...\n")

        start_time = time.time()

        while (time.time() - start_time) < duration_seconds:
            # 检查是否需要休息
            if self.should_take_break():
                self.take_break()

            # 模拟工作
            self.simulate_work()

        elapsed = int(time.time() - start_time)
        self.log(f"\n" + "=" * 60)
        self.log(f"✅ 演示完成")
        self.log(f"📊 统计:")
        self.log(f"   - 总耗时: {elapsed} 秒")
        self.log(f"   - 工作循环: {self.cycle} 次")
        self.log(f"   - 平均循环: {elapsed / self.cycle:.1f} 秒/次")
        self.log("=" * 60 + "\n")


def main():
    print("\n" + "█" * 60)
    print("█                                                          █")
    print("█   Linux.do 刷帖助手 v8.6 - 随机间断功能演示             █")
    print("█                                                          █")
    print("█" * 60 + "\n")

    print("📝 功能说明:")
    print("   - 在运行过程中随机暂停休息，模拟真人使用习惯")
    print("   - 每隔 10-20 分钟随机休息 2-5 分钟（可自定义）")
    print("   - 休息期间显示倒计时，休息时间不计入总运行时间")
    print("   - 完全随机化，增强防检测能力\n")

    input("按回车键开始演示... ")

    demo = BreakFeatureDemo()
    demo.run_demo(duration_seconds=60)

    print("\n" + "=" * 60)
    print("💡 实际使用提示:")
    print("=" * 60)
    print("\n1. 打开 linux_do_gui.py")
    print("2. 找到'运行模式'区域下方的'随机间断配置'")
    print("3. 勾选 ☑ 启用随机间断")
    print("4. 设置间断时间: 2 - 5 分钟（推荐）")
    print("5. 点击'开始'运行\n")

    print("📖 查看详细文档:")
    print("   - BREAK_FEATURE.md      - 功能详细说明")
    print("   - CHANGELOG_v8.6.md     - 更新日志")
    print("   - IMPLEMENTATION_SUMMARY.md - 实现总结")
    print("   - VERIFICATION_CHECKLIST.md - 验证清单\n")

    print("=" * 60)
    print("✨ 感谢使用！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
