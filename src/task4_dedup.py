# -*- coding: utf-8 -*-
"""任务4：去重算法对比（无序去重 vs 保序去重），以及嵌套列表去重。"""

from typing import List


def dedup_unordered(data: List) -> List:
    """方案1：list(set(data))，最简洁，但丢失原始顺序。"""
    return list(set(data))


def dedup_ordered_loop(data: List) -> List:
    """方案2：遍历 + 成员判断，保留第一次出现顺序。"""
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    return result


def dedup_ordered_dict(data: List) -> List:
    """拓展：dict.fromkeys 一行实现保序去重（Python 3.7+ 字典保序）。"""
    return list(dict.fromkeys(data))


def dedup_nested(nest: List[List]) -> List[List]:
    """嵌套列表去重：内层 list 不可哈希，先转元组再判重，最后按需转回列表。"""
    seen = set()
    result = []
    for inner in nest:
        key = tuple(inner)
        if key in seen:
            continue
        seen.add(key)
        result.append(list(key))
    return result


def task4_report() -> dict:
    data = [5, 2, 7, 2, 5, 9, 7, 3, 9, 1]
    nest = [[1, 2], [3, 4], [1, 2], [5, 6]]
    return {
        "source": data,
        "unordered": dedup_unordered(data),
        "ordered_loop": dedup_ordered_loop(data),
        "ordered_dict": dedup_ordered_dict(data),
        "same_element_set": set(dedup_unordered(data)) == set(dedup_ordered_loop(data)),
        "nest_source": nest,
        "nest_deduped": dedup_nested(nest),
    }
