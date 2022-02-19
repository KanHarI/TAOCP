from __future__ import annotations

import math
import random
import sys


class IntegerSqrt2:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def clone(self) -> IntegerSqrt2:
        return IntegerSqrt2(self.a, self.b)

    def __iadd__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        self.a += other.a
        self.b += other.b
        return self

    def __add__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        result = self.clone()
        result += other
        return result

    def __neg__(self) -> IntegerSqrt2:
        return IntegerSqrt2(-self.a, -self.b)

    def __isub__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        self += -other
        return self

    def __sub__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        result = self.clone()
        result -= other
        return result

    def __imul__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        self.a, self.b = (
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )
        return self

    def __mul__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        result = self.clone()
        result *= other
        return result

    def conjugate(self) -> IntegerSqrt2:
        return IntegerSqrt2(self.a, -self.b)

    def mod_norm(self) -> int:
        result = self * self.conjugate()
        assert result.b == 0
        return result.a

    def abs_squared(self) -> int:
        return self.a * self.a + 2 * self.b * self.b

    def __ifloordiv__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        denominator = other.mod_norm()
        numerator = self.clone() * other.conjugate()
        float_a = numerator.a // denominator
        float_b = numerator.b // denominator
        min_norm_squared = math.inf
        min_norm_result = None
        for i in range(4):
            if i % 2 == 0:
                a = float_a
            else:
                a = float_a + 1
            if i // 2 == 0:
                b = float_b
            else:
                b = float_b + 1
            result_candidate = IntegerSqrt2(a, b)
            result_candidate_delta = self - result_candidate * other
            candidate_min_norm_squared = result_candidate_delta.mod_norm() ** 2
            if candidate_min_norm_squared < min_norm_squared:
                min_norm_result = result_candidate
                min_norm_squared = candidate_min_norm_squared
        assert min_norm_result is not None
        self.a = min_norm_result.a
        self.b = min_norm_result.b
        return self

    def __floordiv__(self, other: IntegerSqrt2) -> IntegerSqrt2:
        result = self.clone()
        result //= other
        return result

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.a == other and self.b == 0
        if not isinstance(other, IntegerSqrt2):
            return False
        return self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return repr(self.a) + " + " + repr(self.b) + " sqrt(2)"


def integer_sqrt_2_gcd(m: IntegerSqrt2, n: IntegerSqrt2) -> IntegerSqrt2:
    if n == 0:
        return m
    q = m // n
    r = m - q * n
    return integer_sqrt_2_gcd(n, r)


MAX_TESTING_INT = 1000
NUM_TESTS = 10


def main() -> int:
    for i in range(NUM_TESTS):
        common = IntegerSqrt2(
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
        )
        a = IntegerSqrt2(
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
        )
        b = IntegerSqrt2(
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
            random.randint(-MAX_TESTING_INT, MAX_TESTING_INT),
        )
        m = common * a
        n = common * b
        if m == 0 or n == 0:
            continue
        gcd = integer_sqrt_2_gcd(m, n)
        m_over_gcd = m // gcd
        n_over_gcd = n // gcd
        assert m_over_gcd * gcd == m
        assert n_over_gcd * gcd == n
        assert gcd.mod_norm() ** 2 >= common.mod_norm() ** 2
        print("a:", a, "b:", b, "common:", common, "gcd:", gcd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
