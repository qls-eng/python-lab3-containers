# -*- coding: utf-8 -*-
"""实验三 单元测试：覆盖五个任务，含边界与异常用例。

运行：python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.task1_slice_delete import (
    delete_by_slice,
    remove_even_safely,
    remove_even_while_iterating,
    remove_even_with_while,
    removed_indices,
)
from src.task2_hash import nested_set_demo, probe_hashable, tuple_mutation_demo
from src.task3_set_ops import set_operations, multiples_of_four
from src.task4_dedup import (
    dedup_nested,
    dedup_ordered_dict,
    dedup_ordered_loop,
    dedup_unordered,
)
from src.task5_course_stats import course_stats


class TestTask1SliceDelete(unittest.TestCase):
    """任务1：切片删除与循环删除缺陷。"""

    def test_step_three_from_zero(self):
        self.assertEqual(removed_indices(10, slice(None, None, 3)), [0, 3, 6, 9])
        self.assertEqual(
            delete_by_slice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], slice(None, None, 3)),
            [1, 2, 4, 5, 7, 8],
        )

    def test_step_three_from_one(self):
        self.assertEqual(removed_indices(10, slice(1, None, 3)), [1, 4, 7])
        self.assertEqual(
            delete_by_slice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], slice(1, None, 3)),
            [0, 2, 3, 5, 6, 8, 9],
        )

    def test_negative_step(self):
        self.assertEqual(removed_indices(6, slice(None, None, -2)), [5, 3, 1])
        self.assertEqual(delete_by_slice([0, 1, 2, 3, 4, 5], slice(None, None, -2)), [0, 2, 4])

    def test_reverse_slice_deletes_all(self):
        """边界：del ls[::-1] 会删除全部元素。"""
        self.assertEqual(delete_by_slice([1, 2, 3], slice(None, None, -1)), [])

    def test_delete_does_not_mutate_source(self):
        source = [0, 1, 2, 3, 4, 5]
        delete_by_slice(source, slice(None, None, 2))
        self.assertEqual(source, [0, 1, 2, 3, 4, 5])

    def test_loop_remove_skips_consecutive_even(self):
        """边界：连续偶数时边遍历边删除会漏删。"""
        self.assertEqual(remove_even_while_iterating([2, 4, 6]), [4])
        self.assertEqual(remove_even_while_iterating([1, 2, 3, 4, 5, 6]), [1, 3, 5])

    def test_safe_remove_even(self):
        self.assertEqual(remove_even_safely([2, 4, 6]), [])
        self.assertEqual(remove_even_with_while([2, 4, 6]), [])
        self.assertEqual(remove_even_safely([1, 2, 3, 4, 5, 6]), [1, 3, 5])

    def test_empty_sequence(self):
        """异常：空列表切片删除不报错。"""
        self.assertEqual(removed_indices(0, slice(None, None, 2)), [])
        self.assertEqual(delete_by_slice([], slice(None, None, 2)), [])


class TestTask2Hashable(unittest.TestCase):
    """任务2：可哈希判定。"""

    def test_int_tuple_hashable(self):
        self.assertTrue(probe_hashable((1, 2, 3))["ok"])

    def test_tuple_with_list_unhashable(self):
        result = probe_hashable((1, [2, 3]))
        self.assertFalse(result["ok"])
        self.assertIn("unhashable", result["error"])

    def test_list_unhashable(self):
        result = probe_hashable([1, 2])
        self.assertFalse(result["ok"])
        self.assertIn("unhashable", result["error"])

    def test_frozenset_hashable(self):
        self.assertTrue(probe_hashable(frozenset({1, 2}))["ok"])

    def test_plain_set_unhashable(self):
        result = probe_hashable({1, 2})
        self.assertFalse(result["ok"])
        self.assertIn("unhashable", result["error"])

    def test_nested_set_with_frozenset(self):
        nested = nested_set_demo()
        self.assertEqual(nested["size"], 2)
        self.assertIn(frozenset({1, 2}), nested["nested"])

    def test_tuple_reference_mutable(self):
        demo = tuple_mutation_demo()
        self.assertEqual(demo["tuple"], (1, [2, 3, 4]))
        self.assertFalse(demo["hashable"])


class TestTask3SetOps(unittest.TestCase):
    """任务3：集合运算与集合推导式。"""

    def setUp(self):
        self.a = {2, 4, 6, 8, 10, 12}
        self.b = {3, 6, 9, 12, 15}

    def test_intersection(self):
        self.assertEqual(set_operations(self.a, self.b)["intersection"], {6, 12})

    def test_union(self):
        self.assertEqual(
            set_operations(self.a, self.b)["union"],
            {2, 3, 4, 6, 8, 9, 10, 12, 15},
        )

    def test_differences(self):
        ops = set_operations(self.a, self.b)
        self.assertEqual(ops["a_minus_b"], {2, 4, 8, 10})
        self.assertEqual(ops["b_minus_a"], {3, 9, 15})

    def test_symmetric_difference(self):
        self.assertEqual(
            set_operations(self.a, self.b)["symmetric_difference"],
            {2, 3, 4, 8, 9, 10, 15},
        )

    def test_multiples_of_four(self):
        self.assertEqual(multiples_of_four(1, 30), {4, 8, 12, 16, 20, 24, 28})

    def test_empty_interval(self):
        """边界：区间为空时集合推导式返回空集合。"""
        self.assertEqual(multiples_of_four(5, 3), set())


class TestTask4Dedup(unittest.TestCase):
    """任务4：去重方案对比与嵌套去重。"""

    def setUp(self):
        self.data = [5, 2, 7, 2, 5, 9, 7, 3, 9, 1]

    def test_unordered_dedup_content(self):
        result = dedup_unordered(self.data)
        self.assertEqual(len(result), 6)
        self.assertEqual(sorted(result), [1, 2, 3, 5, 7, 9])

    def test_ordered_loop(self):
        self.assertEqual(dedup_ordered_loop(self.data), [5, 2, 7, 9, 3, 1])

    def test_ordered_dict(self):
        self.assertEqual(dedup_ordered_dict(self.data), [5, 2, 7, 9, 3, 1])

    def test_two_ordered_methods_agree(self):
        self.assertEqual(dedup_ordered_loop(self.data), dedup_ordered_dict(self.data))

    def test_nested_list_dedup(self):
        nest = [[1, 2], [3, 4], [1, 2], [5, 6]]
        self.assertEqual(dedup_nested(nest), [[1, 2], [3, 4], [5, 6]])

    def test_nested_dedup_keeps_original_unchanged(self):
        nest = [[1, 2], [1, 2]]
        dedup_nested(nest)
        self.assertEqual(nest, [[1, 2], [1, 2]])

    def test_empty_list(self):
        """异常：空列表去重返回空列表。"""
        self.assertEqual(dedup_ordered_loop([]), [])
        self.assertEqual(dedup_unordered([]), [])


class TestTask5CourseStats(unittest.TestCase):
    """任务5：综合设计题。"""

    def setUp(self):
        self.class1 = [101, 103, 105, 107, 109, 103, 101]
        self.class2 = [102, 104, 106, 108, 109, 107, 102]
        self.result = course_stats(self.class1, self.class2)

    def test_unique_preserve_order(self):
        self.assertEqual(self.result["class1_unique"], [101, 103, 105, 107, 109])
        self.assertEqual(self.result["class2_unique"], [102, 104, 106, 108, 109, 107])

    def test_both_classes(self):
        self.assertEqual(self.result["both"], [107, 109])

    def test_only_one_class(self):
        self.assertEqual(self.result["only_one"], [101, 102, 103, 104, 105, 106, 108])

    def test_only_class1(self):
        self.assertEqual(self.result["only_class1"], [101, 103, 105])

    def test_intersection_as_tuple_and_set(self):
        self.assertEqual(self.result["both_tuple"], (107, 109))
        self.assertEqual(self.result["both_as_set"], {107, 109})
        self.assertIsInstance(self.result["both_tuple"], tuple)

    def test_tuple_can_join_set(self):
        """⑤ 交集的整数元组可哈希，能再放回集合。"""
        holder = {self.result["both_tuple"]}
        self.assertIn((107, 109), holder)

    def test_empty_input(self):
        """异常：两班都没有学生时结果全为空。"""
        empty = course_stats([], [])
        self.assertEqual(empty["both"], [])
        self.assertEqual(empty["only_one"], [])
        self.assertEqual(empty["both_tuple"], ())


if __name__ == "__main__":
    unittest.main()
