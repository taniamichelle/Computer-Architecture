# Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.
# For example, given the following object/dictionary as input:

a = {
    "cat": "bob",
    "dog": 23,
    19: 18,
    90: "fish"
}

# Your algorithm should return 41, the sum of the values 23 and 18.
# You may use whatever programming language you'd like.

integers = []
int_sum = sum(integers)
for x in a:
    if type(a[x]) == int:
        integers.append(a[x])
        # integer_sum = sum(integers)
        return int_sum