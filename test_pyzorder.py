#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import unittest
import sys
try:
    from time import perf_counter
except ImportError:
    from time import time as perf_counter


class TestPyZorder(unittest.TestCase):
    def test_next_zorder_index_simple(self):
        from pyzorder import ZOrderIndexer
        z_obj = ZOrderIndexer((0, 5), (0, 5))

        correct = sorted([z_obj.zindex(r, c) for r in range(5 + 1) for c in range(5 + 1)])
        i = z_obj.min_z
        ans = [i]
        while i < z_obj.max_z:
            i = z_obj.next_zorder_index_simple(i)
            ans.append(i)
        ans = sorted(ans)
        self.assertListEqual(correct, ans)

    def test_next_zorder_index(self):
        from pyzorder import ZOrderIndexer

        z_obj = ZOrderIndexer((0, 5), (0, 5))
        correct = sorted([z_obj.zindex(r, c) for r in range(5 + 1) for c in range(5 + 1)])
        i = z_obj.min_z
        ans = [i]
        while i < z_obj.max_z and len(ans) <= len(correct):
            i = z_obj.next_zorder_index(i)
            ans.append(i)
        ans = sorted(ans)
        self.assertListEqual(correct, ans)

        z_obj = ZOrderIndexer((2, 4), (2, 5))
        correct = sorted([z_obj.zindex(r, c) for r in range(2, 4 + 1) for c in range(2, 5 + 1)])
        i = z_obj.min_z
        ans = [i]
        while i < z_obj.max_z and len(ans) <= len(correct):
            i = z_obj.next_zorder_index(i)
            ans.append(i)
        ans = sorted(ans)
        self.assertListEqual(correct, ans)

        z_obj = ZOrderIndexer((2, 13), (66, 76))
        correct = sorted([z_obj.zindex(r, c) for r in range(2, 13 + 1) for c in range(66, 76 + 1)])
        i = z_obj.min_z
        ans = [i]
        while i < z_obj.max_z and len(ans) <= len(correct):
            i = z_obj.next_zorder_index(i)
            ans.append(i)
        ans = sorted(ans)
        self.assertListEqual(correct, ans)

    def test_next_zorder_index_atrandom_list(self):
        import random
        from pyzorder import ZOrderIndexer

        max_v = 99
        for test_counter in range(10):
            p1 = sorted([random.randint(0, max_v), random.randint(0, max_v)])
            p2 = sorted([random.randint(0, max_v), random.randint(0, max_v)])
            print(p1, p2, end=" ")
            z_obj = ZOrderIndexer(p1, p2)
            # prepare correct data
            t0 = perf_counter()
            correct = sorted([z_obj.zindex(r, c) for r in range(p1[0], p1[1]+1) for c in range(p2[0], p2[1]+1)])
            t1 = perf_counter()
            print("correct data: %.2fs, " % (t1 - t0), end='')
            # efficient implementation
            t0 = perf_counter()
            i = z_obj.min_z
            ans = [i]
            while i < z_obj.max_z and len(ans) <= len(correct):
                i = z_obj.next_zorder_index(i)
                ans.append(i)
            ans = sorted(ans)
            t1 = perf_counter()
            print("efficient: %.2fs [%.2fus], " % (t1 - t0, (t1 - t0) / len(ans) * 1000000), end='')
            self.assertListEqual(correct, ans)
            # simple implementation
            t0 = perf_counter()
            i = z_obj.min_z
            ans = [i]
            while i < z_obj.max_z:
                i = z_obj.next_zorder_index_simple(i)
                ans.append(i)
            ans = sorted(ans)
            t1 = perf_counter()
            print("simple: %.2fs [%.2fus], " % (t1 - t0, (t1 - t0) / len(ans) * 1000000), end='')
            self.assertListEqual(correct, ans)
            print()

    def test_next_zorder_index_atrandom(self):
        import random
        from pyzorder import ZOrderIndexer

        if getattr(sys, 'maxint', 0) and sys.maxint <= 2 ** 31 - 1:
            max_v = 0x0fff
        else:
            max_v = 0x0fffffff

        for test_counter in range(100):
            p1 = sorted([random.randint(0, max_v), random.randint(0, max_v), random.randint(0, max_v)])
            p2 = sorted([random.randint(0, max_v), random.randint(0, max_v), random.randint(0, max_v)])
            print(p1, p2, end=" ")
            z_obj = ZOrderIndexer(p1[::2], p2[::2])
            z_key = z_obj.zindex(p1[1], p2[1])

            # efficient implementation
            t0 = perf_counter()
            ans1 = z_obj.next_zorder_index(z_key)
            t1 = perf_counter()
            print("efficient: %.2f us, " % ((t1 - t0) * 1000000), end='')
            # simple implementation
            t0 = perf_counter()
            ans2 = z_obj.next_zorder_index_simple(z_key)
            t1 = perf_counter()
            print("simple: %.2f us, " % ((t1 - t0) * 1000000), end='')
            # compare the results
            self.assertEqual(ans1, ans2)
            print()


if __name__ == '__main__':
    unittest.main()
