def twos_complement_inverse(x, bits):
    if bits <= 0:
        raise ValueError("Number of bits must be greater than 0")

    max_value = 2**bits
    if x >= max_value:
        raise ValueError(f"Value out of range for {bits}-bit number")
    
    if x < 0:
        raise ValueError("Input must be a non-negative integer")

    # Check if the number is in the negative range in two's complement
    if x >= 2**(bits - 1):
        x -= 2**bits

    return x

# Examples for 32-bit integers
examples = [0, 1, 127, 128, 129, 255, 2147483647, 2147483648, 2147483649, 4294967295]

for x in examples:
    print(f"{x} -> {twos_complement_inverse(x, 32)}")