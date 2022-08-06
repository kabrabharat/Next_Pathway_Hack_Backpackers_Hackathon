def get_BitCompress(bits_str):
    rev_bits = reverse(bits_str)
    temp = rev_bits
    ans = 0
    for rev_bit in temp:
        if rev_bit == '1':
            index = indexOf(rev_bits, 1)
            rev_bits = rev_bits[index+1:]
            ans += Pwr(2, index)
    return ans