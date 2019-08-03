#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from . import pymorton

# use xrange as range in Python2 environment
try:
    # noinspection PyShadowingBuiltins
    range = xrange  # python 2
except NameError:
    pass  # python 3


class ZOrderIndexer:
    def __init__(self, row_range, col_range):
        self.row_min, self.row_max = row_range
        self.col_min, self.col_max = col_range

        self.min_z = self.zindex(self.row_min, self.col_min)
        self.max_z = self.zindex(self.row_max, self.col_max)

        if getattr(sys, 'maxint', 0) and sys.maxint <= 2 ** 31 - 1:
            self.bit_position_init = 0x80000000
            self.load_mask_init = 0x55555555
            self.load_ones_init = 0x2aaaaaaa
        else:
            self.bit_position_init = 0x8000000000000000
            self.load_mask_init = 0x5555555555555555
            self.load_ones_init = 0x2aaaaaaaaaaaaaaa

    @staticmethod
    def zindex(r, c):
        return pymorton.interleave(r, c)

    @staticmethod
    def rc(z):
        r, c = pymorton.deinterleave2(z)
        return r, c

    def is_in(self, z):
        r, c = self.rc(z)
        return (self.row_min <= r <= self.row_max) and (self.col_min <= c <= self.col_max)

    def next_zorder_index(self, z):
        """
        return z-order index next to given z (BIGMIN)
        :param z: key z-index
        :return: z-order index next to given z (BIGMIN)
        """
        if self.is_in(z + 1):
            return z + 1

        min_v = self.min_z
        max_v = self.max_z
        bit_position = self.bit_position_init  # 10000000..  bit position currently investigating
        load_mask = self.load_mask_init     # 01010101..  original value preserving mask
        load_ones = self.load_ones_init     # 00101010..  loading value for LOAD(0111..)

        while bit_position:
            z_bit, min_bit, max_bit = z & bit_position, min_v & bit_position, max_v & bit_position
            # decision table from the paper
            if not z_bit and not min_bit and not max_bit:  # 0 0 0
                pass
            elif not z_bit and not min_bit and max_bit:  # 0 0 1
                bigmin = min_v & load_mask | bit_position
                max_v = max_v & load_mask | load_ones
            elif not z_bit and min_bit and max_bit:  # 0 1 1
                return int(min_v)
            elif z_bit and not min_bit and not max_bit:  # 1 0 0
                # noinspection PyUnboundLocalVariable
                return int(bigmin)
            elif z_bit and not min_bit and max_bit:  # 1 0 1
                min_v = min_v & load_mask | bit_position
            elif z_bit and min_bit and max_bit:  # 1 1 1
                pass
            else:  # 0 1 0 or 1 1 0
                # it should be never happen..
                raise ValueError('Z-order index search failed. Something wrong...')

            # investigate next bit position
            bit_position >>= 1
            load_ones >>= 1
            load_mask >>= 1
            load_mask |= self.bit_position_init

        # noinspection PyUnboundLocalVariable
        return int(bigmin)

    def next_zorder_index_simple(self, z):
        """
        return z-order index next to given z with quite simple implementation (BIGMIN)
        :param z: key z-index
        :return: z-order index next to given z (BIGMIN)
        """

        if (z < self.min_z) or (self.max_z <= z):
            raise ValueError

        # searching valid z-index one by one
        for i in range(z + 1, self.max_z + 1):
            if self.is_in(i):
                return i

        raise ValueError('Z-order index search failed. Something wrong...')
