#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试随机间断功能
"""

import time
from datetime import datetime


class MockBot:
    """模拟 Bot 类以测试间断逻辑"""

    def __init__(self, enable_break=True, break_min=2, break_max=5):
        self.enable_break = enable_break
        self.break_min = break_min
        self.break_max = break_max
        self.run = True
        self.last_break_time = None
        self.next_break_interval = None

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def _schedule_next_break(self):
        """计算下次间断的时间间隔（分钟）"""
        if not self.enable_break:
            return None
        # 为了测试，设置为 0.5-1 分钟（30-60秒）
        import random
        interval = random.uniform(0.5, 1)
        self.log(f"💤 已安排下次休息：约 {int(interval * 60)} 秒后")
        return interval

    def _should_take_break(self):
        """检查是否应该进行间断"""
        if not self.enable_break or not self.run:
            return False

        # 第一次运行，设置下次间断时间
        if self.last_break_time is None:
            self.last_break_time = time.time()
            self.next_break_interval = self._schedule_next_break()
            return False

        # 计算距离上次间断的时间（分钟）
        elapsed_minutes = (time.time() - self.last_break_time) / 60

        # 检查是否到达间断时间
        if self.next_break_interval and elapsed_minutes >= self.next_break_interval:
            return True

        return False

    def _take_break(self):
        """执行随机间断"""
        if not self.run:
            return

        import random
        # 为了测试，设置为 5-10 秒
        break_duration = random.uniform(5, 10)
        break_seconds = int(break_duration)

        self.log("=" * 30)
        self.log(f"💤 开始休息 {break_seconds} 秒（测试模式）")
        self.log("=" * 30)

        # 倒计时显示
        start_break = time.time()
        while self.run and (time.time() - start_break) < break_seconds:
            remaining = break_seconds - int(time.time() - start_break)
            print(f"\r💤 休息中: {remaining} 秒剩余", end="", flush=True)
            time.sleep(1)

        print()  # 换行

        if self.run:
            self.log("=" * 30)
            self.log("✨ 休息结束，继续工作")
            self.log("=" * 30)

        # 更新间断记录，安排下次间断
        self.last_break_time = time.time()
        self.next_break_interval = self._schedule_next_break()

    def test_run(self, duration_seconds=120):
        """测试运行指定秒数"""
        self.log(f"开始测试，运行 {duration_seconds} 秒")
        self.log(f"间断配置: 启用={self.enable_break}, 间隔=0.5-1分钟, 时长={self.break_min}-{self.break_max}分钟")
        self.log("=" * 30)

        start_time = time.time()
        cycle = 0

        while self.run and (time.time() - start_time) < duration_seconds:
            # 检查是否需要间断
            if self._should_take_break():
                self._take_break()

            if not self.run:
                break

            # 模拟工作
            cycle += 1
            self.log(f"工作循环 #{cycle}")
            time.sleep(5)  # 每个工作循环 5 秒

        elapsed = time.time() - start_time
        self.log("=" * 30)
        self.log(f"测试完成，总耗时: {int(elapsed)} 秒")


def main():
    print("=" * 50)
    print("随机间断功能测试")
    print("=" * 50)
    print()

    # 测试 1: 启用间断
    print("测试 1: 启用随机间断（运行 120 秒）")
    print("-" * 50)
    bot1 = MockBot(enable_break=True, break_min=2, break_max=5)
    bot1.test_run(duration_seconds=120)

    print()
    print("=" * 50)
    print()

    # 测试 2: 禁用间断
    print("测试 2: 禁用随机间断（运行 30 秒）")
    print("-" * 50)
    bot2 = MockBot(enable_break=False)
    bot2.test_run(duration_seconds=30)

    print()
    print("=" * 50)
    print("✓ 所有测试完成")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
