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


#compress function after building the Huffman tree
def Compress (data,codes):
    ret=""
    for c in data:
        ret+=codes[c]
    return ret



#Decompress function using the huffman codes that we get




# Example usage
data = "sddkndss"
freq = calc_freq(data)
huffman_root = buildHuffman(freq)
huffman_codes = get_codes(huffman_root)
compressed=Compress(data,huffman_codes)

print("Huffman Codes:", huffman_codes)
print("Compressed:", compressed)




