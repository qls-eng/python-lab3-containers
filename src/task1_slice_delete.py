# -*- coding: utf-8 -*-
"""任务1：切片删除深度探究。

验证 del 列表[切片] 的索引是按删除前的原始列表一次性计算，
而不是删除过程中动态实时计算的。
"""

from typing import List, Sequence


def removed_indices(length: int, sl: slice) -> List[int]:
    """按切片在原始序列上一次性算出将删除的索引。

    slice.indices(length) 会把 start/stop/step 规范化为可以套进 range 的三元组，
    负步长、省略端点都由它处理，因此这里算出的就是删除前的原始索引。
    """
    return list(range(*sl.indices(length)))


def delete_by_slice(seq: Sequence, sl: slice) -> List:
    """返回删除切片元素后的新列表，不修改传入的序列。"""
    removed = set(removed_indices(len(seq), sl))
    return [item for index, item in enumerate(seq) if index not in removed]


def remove_even_while_iterating(seq: Sequence) -> List[int]:
    """复现「边 for 遍历边 remove」的缺陷写法，用于对比分析。"""
    data = list(seq)
    for item in data:
        if item % 2 == 0:
            data.remove(item)
    return data


def remove_even_safely(seq: Sequence) -> List[int]:
    """安全写法一：列表推导式生成新列表，遍历的是原序列。"""
    return [item for item in seq if item % 2 != 0]


def remove_even_with_while(seq: Sequence) -> List[int]:
    """安全写法二：显式下标 + while，删除后不移动下标。"""
    data = list(seq)
    index = 0
    while index < len(data):
        if data[index] % 2 == 0:
            del data[index]
        else:
            index += 1
    return data


def task1_cases() -> List[dict]:
    """任务1 的三组切片删除用例，含预判值与实际值。"""
    cases = [
        {
            "name": "del ls1[::3]",
            "source": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "slice": slice(None, None, 3),
            "expect": [1, 2, 4, 5, 7, 8],
            "reason": "从索引 0 起每隔 3 个删一个，删除索引 0、3、6、9",
        },
        {
            "name": "del ls2[1::3]",
            "source": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "slice": slice(1, None, 3),
            "expect": [0, 2, 3, 5, 6, 8, 9],
            "reason": "起点 1，步长 3，删除索引 1、4、7",
        },
        {
            "name": "del ls3[::-2]",
            "source": [0, 1, 2, 3, 4, 5],
            "slice": slice(None, None, -2),
            "expect": [0, 2, 4],
            "reason": "负步长从末尾往前，删除索引 5、3、1",
        },
    ]
    for case in cases:
        case["removed"] = removed_indices(len(case["source"]), case["slice"])
        case["actual"] = delete_by_slice(case["source"], case["slice"])
    return cases


def task1_report() -> dict:
    """汇总任务1 的验证结果。"""
    return {
        "cases": task1_cases(),
        "loop_source": [1, 2, 3, 4, 5, 6],
        "loop_actual": remove_even_while_iterating([1, 2, 3, 4, 5, 6]),
        "loop_safe": remove_even_safely([1, 2, 3, 4, 5, 6]),
        "loop_while": remove_even_with_while([1, 2, 3, 4, 5, 6]),
        "consecutive_source": [2, 4, 6],
        "consecutive_actual": remove_even_while_iterating([2, 4, 6]),
    }
