# -*- coding: utf-8 -*-
"""任务3：集合全部运算与集合推导式。"""

A = {2, 4, 6, 8, 10, 12}
B = {3, 6, 9, 12, 15}


def set_operations(a: set, b: set) -> dict:
    """返回交集、并集、A-B、B-A、对称差集五种结果。"""
    return {
        "intersection": a & b,
        "union": a | b,
        "a_minus_b": a - b,
        "b_minus_a": b - a,
        "symmetric_difference": a ^ b,
    }


def multiples_of_four(start: int = 1, end: int = 30) -> set:
    """集合推导式：生成 [start, end] 区间内能被 4 整除的数。"""
    return {x for x in range(start, end + 1) if x % 4 == 0}


def task3_report() -> dict:
    ops = set_operations(A, B)
    return {
        "A": A,
        "B": B,
        "operations": ops,
        "multiples_of_four": multiples_of_four(1, 30),
        "check": {
            "intersection_literal": {6, 12},
            "union_size": len(ops["union"]),
            "symmetric_equals_either_only": ops["symmetric_difference"] == (A | B) - (A & B),
        },
    }
