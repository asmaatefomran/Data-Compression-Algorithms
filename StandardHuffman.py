import heapq
from collections import defaultdict


# Calculate the frequency of characters in the data
def calc_freq(data):
    fr = defaultdict(int)
    for c in data:
        fr[c] += 1
    return fr


class HufNode:
    def __init__(self, fr, char=None, left=None, right=None):
        self.fr = fr
        self.char = char
        self.l = left
        self.r = right

    def __lt__(self, other):
        return self.fr < other.fr


# Build the Huffman tree using a priority queue (min-heap)
def buildHuffman(fr):
    pq = []
    for char, freq in fr.items():
        heapq.heappush(pq, HufNode(freq, char))

    while len(pq) > 1:
        left = heapq.heappop(pq)
        right = heapq.heappop(pq)
        merged = HufNode(left.fr + right.fr, None, left, right)
        heapq.heappush(pq, merged)

    return pq[0] if pq else None


# Recursively generate Huffman codes from the Huffman tree
def get_codes(node, currcode="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return

    if node.char is not None:
        codes[node.char] = currcode
    else:
        get_codes(node.l, currcode + '0', codes)
        get_codes(node.r, currcode + '1', codes)

    return codes


# Reverse the codes map so it can be used by Decompress function
def reverseMap(codes):
    reversed_map = {}
    for c, code in codes.items():
        reversed_map[code] = c

    return reversed_map


# Compress function after building the Huffman tree
def Compress(data, codes):
    ret = ""
    for c in data:
        ret += codes[c]
    return ret


# Decompress function using the Huffman codes
def Decompress(compData, codes):
    nwcodes = reverseMap(codes)

    curr = ""
    ret = ""
    start = 0
    while start < len(compData):
        curr += compData[start]
        if curr in nwcodes:
            ret += nwcodes[curr]
            curr = ""
        start += 1
    return ret


# Compress function for files
def compress_file(input_file, compressed_file, codes_file):
    with open(input_file, 'r') as infile:
        data = infile.read()

    freq = calc_freq(data)
    huffman_root = buildHuffman(freq)
    huffman_codes = get_codes(huffman_root)
    compressed_data = Compress(data, huffman_codes)

    with open(compressed_file, 'w') as outfile:
        outfile.write(compressed_data)
    with open(codes_file, 'w') as codes_outfile:
        for char, code in huffman_codes.items():
            char_representation = 'SPACE' if char == ' ' else char
            codes_outfile.write(f"{char_representation}:{code}\n")


# Decompress function for files
def decompress_file(compressed_file, codes_file, output_file):
    with open(compressed_file, 'r') as infile:
        compressed_data = infile.read()

    codes = {}
    with open(codes_file, 'r') as codes_infile:
        for line in codes_infile:
            char, code = line.strip().split(':', 1)
            char = ' ' if char == 'SPACE' else char
            codes[char] = code

    decompressed_data = Decompress(compressed_data, codes)

    with open(output_file, 'w') as outfile:
        outfile.write(decompressed_data)


# Test for file operations
def test_file_operations():
    input_filename = 'test_input.txt'
    compressed_filename = 'test_compressed.txt'
    codes_filename = 'test_codes.txt'
    decompressed_filename = 'test_decompressed.txt'
    test_data = "asmaa atef with file"

    with open(input_filename, 'w') as infile:
        infile.write(test_data)

    print("\nTesting file compression...")
    compress_file(input_filename, compressed_filename, codes_filename)

    with open(compressed_filename, 'r') as compressed_file:
        compressed_data = compressed_file.read()
    print("Compressed Data:", compressed_data)

    print("Huffman Codes:")
    with open(codes_filename, 'r') as codes_file:
        codes_data = codes_file.readlines()
    for line in codes_data:
        print(line.strip())

    print("\nTesting file decompression...")
    decompress_file(compressed_filename, codes_filename, decompressed_filename)

    with open(decompressed_filename, 'r') as decompressed_file:
        decompressed_data = decompressed_file.read()
    print("Decompressed Data:", decompressed_data)

    # Verify correctness
    assert decompressed_data == test_data, "File decompression failed!"
    print("\nFile compression and decompression test passed successfully!")


# Test for in-memory operations
def test_logic():
    test_data = "asmaa atef without file"
    freq = calc_freq(test_data)
    huffman_root = buildHuffman(freq)
    huffman_codes = get_codes(huffman_root)
    compressed_data = Compress(test_data, huffman_codes)

    print("\nLogic Test Results:")
    print("Huffman Codes:", huffman_codes)
    print("Compressed Data:", compressed_data)

    decompressed_data = Decompress(compressed_data, huffman_codes)
    print("Decompressed Data:", decompressed_data)

    assert decompressed_data == test_data, "Logic decompression failed!"
    print("\nLogic test passed successfully!")


# Run tests
test_logic()
test_file_operations()
