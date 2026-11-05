# -*- coding: utf-8 -*-
"""实验主程序：一次性运行五个任务并打印报告。

运行：python src/main.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.task1_slice_delete import task1_report
from src.task2_hash import task2_report
from src.task3_set_ops import task3_report
from src.task4_dedup import task4_report
from src.task5_course_stats import task5_report


def print_task1(report: dict) -> None:
    print("===== 任务1 切片删除深度探究 =====")
    for case in report["cases"]:
        print(f"{case['name']} 源列表 {case['source']}")
        print(f"  删除索引（删除前一次性计算）：{case['removed']}")
        print(f"  预判：{case['expect']}")
        print(f"  实际：{case['actual']}  一致={case['actual'] == case['expect']}")
        print(f"  原因：{case['reason']}")

    print(f"遍历中删除 {report['loop_source']} 的偶数 → {report['loop_actual']}")
    print(f"  安全写法（推导式）→ {report['loop_safe']}")
    print(f"  安全写法（while 下标）→ {report['loop_while']}")
    print(f"连续偶数 {report['consecutive_source']} → {report['consecutive_actual']}"
          "（漏删，说明缺陷真实存在）")


def print_task2(report: dict) -> None:
    print("\n===== 任务2 可哈希辨析 =====")
    for case in report["cases"]:
        status = "成功加入" if case["ok"] else "报错"
        print(f"{case['label']:<24} {status:<8} 预期={case['expect_ok']}")
        if case["error"]:
            print(f"  错误信息：{case['error']}")
        print(f"  理由：{case['reason']}")

    nested = report["nested"]
    print(f"frozenset 嵌套集合：{nested['nested']}，元素个数 {nested['size']}")
    print(f"内层交集 {nested['intersection']}，内层并集 {nested['union']}")
    print(f"说明：{nested['note']}")

    mutation = report["mutation"]
    print(f"元组内含列表：{mutation['tuple']}，append 后内层 {mutation['inner_after_append']}")
    print(f"说明：{mutation['note']}")


def print_task3(report: dict) -> None:
    print("\n===== 任务3 集合运算与推导式 =====")
    print(f"A = {report['A']}，B = {report['B']}")
    ops = report["operations"]
    print(f"交集 A & B = {ops['intersection']}")
    print(f"并集 A | B = {ops['union']}")
    print(f"差集 A - B = {ops['a_minus_b']}")
    print(f"差集 B - A = {ops['b_minus_a']}")
    print(f"对称差 A ^ B = {ops['symmetric_difference']}")
    print(f"1~30 内能被 4 整除的集合：{report['multiples_of_four']}")
    print(f"对称差校验：{report['check']['symmetric_equals_either_only']}")


def print_task4(report: dict) -> None:
    print("\n===== 任务4 去重方案对比 =====")
    print(f"原始数据：{report['source']}")
    print(f"方案1 list(set(data))：{report['unordered']}（顺序不可控）")
    print(f"方案2 手写保序去重：{report['ordered_loop']}")
    print(f"拓展 dict.fromkeys：{report['ordered_dict']}")
    print(f"两者元素集合一致：{report['same_element_set']}")
    print(f"嵌套列表去重：{report['nest_source']} → {report['nest_deduped']}")


def print_task5(report: dict) -> None:
    print("\n===== 任务5 综合设计：两班选课统计 =====")
    print(f"1 班原始：{report['class1']}")
    print(f"2 班原始：{report['class2']}")
    print(f"① 1 班不重复编号（保序）：{report['class1_unique']}")
    print(f"① 2 班不重复编号（保序）：{report['class2_unique']}")
    print(f"② 同时选两门：{report['both']}")
    print(f"③ 只选其中一门（对称差）：{report['only_one']}")
    print(f"④ 选了 1 班没选 2 班：{report['only_class1']}")
    print(f"⑤ 交集转元组：{report['both_tuple']}")
    print(f"⑤ 元组转回集合：{report['both_as_set']}")
    for line in report["explain"]:
        print(f"  {line}")


def main() -> None:
    print_task1(task1_report())
    print_task2(task2_report())
    print_task3(task3_report())
    print_task4(task4_report())
    print_task5(task5_report())


if __name__ == "__main__":
    main()
