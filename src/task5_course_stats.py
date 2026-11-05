# -*- coding: utf-8 -*-
"""任务5：综合设计题——两班选课编号统计（必做）。"""

from typing import List, Tuple

from src.task4_dedup import dedup_ordered_loop


def course_stats(class1: List[int], class2: List[int]) -> dict:
    """完成五个小问：保序去重、交集、对称差、差集、交集转元组。"""
    unique1 = dedup_ordered_loop(class1)
    unique2 = dedup_ordered_loop(class2)

    set1 = set(class1)
    set2 = set(class2)
    both = set1 & set2                    # ② 同时选两门
    only_one = set1 ^ set2                # ③ 只选其中一门
    only_class1 = set1 - set2             # ④ 选 1 班没选 2 班

    both_tuple: Tuple[int, ...] = tuple(sorted(both))   # ⑤ 交集转元组

    return {
        "class1_unique": unique1,
        "class2_unique": unique2,
        "both": sorted(both),
        "only_one": sorted(only_one),
        "only_class1": sorted(only_class1),
        "both_tuple": both_tuple,
        "both_as_set": set(both_tuple),
    }


def explain() -> List[str]:
    """任务5 每一步的文字说明，供报告直接引用。"""
    return [
        "① 保序去重：遍历原列表，元素没出现过才 append，得到班级独立学生编号集合；",
        "② 交集 &：同时出现在两个集合中的编号，即同时选两门课的学生；",
        "③ 对称差 ^：只出现在其中一个集合的编号，即只选了一门课的学生；",
        "④ 差集 -：属于 1 班但不属于 2 班的编号；",
        "⑤ 交集元素都是整数（可哈希），转成元组后仍可哈希，所以既能转元组也能再放回集合；"
        "若交集元素含列表，则既不能转元组入集合，也无法作为集合元素。",
    ]


def task5_report() -> dict:
    class1 = [101, 103, 105, 107, 109, 103, 101]
    class2 = [102, 104, 106, 108, 109, 107, 102]
    data = course_stats(class1, class2)
    data["class1"] = class1
    data["class2"] = class2
    data["explain"] = explain()
    return data
