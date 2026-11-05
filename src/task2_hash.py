# -*- coding: utf-8 -*-
"""任务2：嵌套容器与可哈希深度辨析。

逐条把候选对象放进集合：能放进去说明可哈希，抛 TypeError 说明不可哈希。
"""

from typing import List


def probe_hashable(obj) -> dict:
    """把对象尝试放进 set，返回是否成功以及失败原因。"""
    container = set()
    try:
        container.add(obj)
        return {"ok": True, "error": None, "container": container}
    except TypeError as exc:
        return {"ok": False, "error": str(exc), "container": container}


def task2_cases() -> List[dict]:
    """任务2 要求依次测试的五种对象。"""
    cases = [
        {"label": "(1, 2, 3)", "factory": lambda: (1, 2, 3),
         "expect_ok": True, "reason": "元组三个元素都是整数，整数可哈希，元组整体可哈希"},
        {"label": "(1, [2, 3])", "factory": lambda: (1, [2, 3]),
         "expect_ok": False, "reason": "元组内有列表，列表不可哈希，整个元组随之不可哈希"},
        {"label": "[1, 2]", "factory": lambda: [1, 2],
         "expect_ok": False, "reason": "列表可变，hash 值会随内容变化，本身不可哈希"},
        {"label": "frozenset({1, 2})", "factory": lambda: frozenset({1, 2}),
         "expect_ok": True, "reason": "frozenset 不可变，hash 值固定，可作为集合元素"},
        {"label": "{1, 2}", "factory": lambda: {1, 2},
         "expect_ok": False, "reason": "普通 set 可变，不可哈希，也不能嵌套进集合"},
    ]
    results = []
    for case in cases:
        probe = probe_hashable(case["factory"]())
        results.append({
            "label": case["label"],
            "ok": probe["ok"],
            "expect_ok": case["expect_ok"],
            "error": probe["error"],
            "reason": case["reason"],
        })
    return results


def nested_set_demo() -> dict:
    """用 frozenset 实现「集合里放集合」。"""
    a = frozenset({1, 2})
    b = frozenset({3, 4})
    nested = {a, b}
    return {
        "nested": nested,
        "size": len(nested),
        "intersection": a & b,
        "union": a | b,
        "note": "外层必须是 set，内层必须是 frozenset，内层若为 set 会抛 TypeError",
    }


def tuple_mutation_demo() -> dict:
    """演示「元组引用不可变」与「元素内容可变」的区别。"""
    inner = [2, 3]
    t = (1, inner)
    inner.append(4)
    return {
        "tuple": t,
        "inner_after_append": inner,
        "hashable": False,
        "note": "元组保存的是列表的引用，引用地址没变，所以 t[1].append(4) 合法；"
                "但元组内含列表，整体不可哈希，不能放进集合",
    }


def task2_report() -> dict:
    return {
        "cases": task2_cases(),
        "nested": nested_set_demo(),
        "mutation": tuple_mutation_demo(),
    }
