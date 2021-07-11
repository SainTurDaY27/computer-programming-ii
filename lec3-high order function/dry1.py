# Make this code DRY

def num_digits(a):
    a_digits = 0
    while a > 0:
        a = a // 10
        a_digits = a_digits + 1
    return a_digits


def same_length(a, b):
    """Return whether positive integers a and b have the same number of digits."""

    # a_digits = 0
    # while a > 0:
    #     a = a // 10
    #     a_digits = a_digits + 1
    # b_digits = 0
    # while b > 0:
    #     b = b // 10
    #     b_digits = b_digits + 1
    # return a_digits == b_digits

    return num_digits(a) == num_digits(b)


print(same_length(50, 70))
print(same_length(50, 100))
print(same_length(10000, 12345))
