class Packet:
    def __init__(self, l):
        if type(l) == int:
            self.l = l
        else:
            self.l = [Packet(item) for item in l]

    def __str__(self):
        if type(self.l) == int:
            return str(self.l)
        else:
            return str([str(item) for item in self.l])

    def __lt__(self, other):
        if type(self.l) == int and type(other.l) == int:
            return self.l < other.l
        elif type(self.l) == list and type(other.l) == list:
            for i in range(min(len(self.l), len(other.l))):
                if self.l[i] != other.l[i]:
                    return self.l[i] < other.l[i]
            return len(self.l) < len(other.l)
        elif type(self.l) == int:
            tmp = self.l
            self.l = [Packet(self.l)]
            result = self < other
            self.l = tmp
            return result
        else:
            tmp = other.l
            other.l = [Packet(other.l)]
            result = self < other
            other.l = tmp
            return result

    def __eq__(self, other):
        if type(self.l) == int and type(other.l) == int:
            return self.l == other.l
        elif type(self.l) == list and type(other.l) == list:
            for i in range(min(len(self.l), len(other.l))):
                if self.l[i] != other.l[i]:
                    return False
            return len(self.l) == len(other.l)
        elif type(self.l) == int:
            tmp = self.l
            self.l = [Packet(self.l)]
            result = self == other
            self.l = tmp
            return result
        else:
            tmp = other.l
            other.l = [Packet(other.l)]
            result = self == other
            other.l = tmp
            return result


def get_packets():
    packet_pairs = []
    for i, pairs in enumerate(open("input.txt").read().split("\n\n")):
        pairs = pairs.split("\n")
        left = Packet(eval(pairs[0]))
        right = Packet(eval(pairs[1]))
        packet_pairs.append((left, right))

    return packet_pairs

print(sum([i+1 for i, (l, r) in enumerate(get_packets()) if l < r]))

list1, list2 = zip(*get_packets())
divider1 = Packet([[2]])
divider2 = Packet([[6]])
packets = list(list1) + list(list2) + [divider1] + [divider2]
packets = sorted(packets)

print(f"Decoder key: {(packets.index(divider1) + 1) * (packets.index(divider2) + 1)}")
