from functools import lru_cache

class Valve:
    def __init__(self, name, flow_rate=0):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = []

    def __repr__(self):
        return f"{self.name} has flow rate={self.flow_rate} and tunnels lead to valves {', '.join([valve.name for valve in self.neighbors])}"

def get_valves():
    valves = {}
    for line in open("input.txt").readlines():
        first, second = line.split(";")
        valve_name, flow_rate = first.split(" has flow rate=")
        valve_name = valve_name.split("Valve ")[1].strip()
        flow_rate = int(flow_rate)
        _, _, _, _, *neighbors = second.strip().split(" ")
        neighbors = [n.strip()[:2] for n in neighbors]
        if valve_name not in valves:
            valves[valve_name] = Valve(valve_name, flow_rate)
        else:
            valves[valve_name].flow_rate = flow_rate
        for neighbor in neighbors:
            if neighbor not in valves:
                valves[neighbor] = Valve(neighbor)
            valves[valve_name].neighbors.append(valves[neighbor])
    return valves

valves = get_valves()

def argmax(l: list):
    return max(range(len(l)), key=lambda i: l[i])

@lru_cache(maxsize=None)
def get_max_released_pressure(current_rooms: tuple, open_valves: frozenset, time_remaining: int):
    if time_remaining == 0:
        # return 0, open_valves
        return 0

    total_flow = sum([valves[name].flow_rate for name in open_valves])

    # released_pressures = []
    max_pressure = 0
    if len(current_rooms) == 1:
        current_room = current_rooms[0]
        # Try to open the valve in the current room
        if current_room not in open_valves and valves[current_room].flow_rate > 0:
            # released_pressures.append(get_max_released_pressure(current_rooms, open_valves | {current_room}, time_remaining - 1))
            max_pressure = max(max_pressure, get_max_released_pressure(current_rooms, open_valves | {current_room}, time_remaining - 1))
        for n in valves[current_room].neighbors:
            # released_pressures.append(get_max_released_pressure((n.name,), open_valves, time_remaining - 1))
            max_pressure = max(max_pressure, get_max_released_pressure((n.name,), open_valves, time_remaining - 1))
    else:
        for my_choice in valves[current_rooms[0]].neighbors + [valves[current_rooms[0]]]:
            for el_choice in valves[current_rooms[1]].neighbors + [valves[current_rooms[1]]]:
                new_open_valves = set()
                # No point in both opening the same valve.
                if my_choice == valves[current_rooms[0]]:
                    new_open_valves.add(current_rooms[0])
                if el_choice == valves[current_rooms[1]]:
                    new_open_valves.add(current_rooms[1])

                # No point opening a valve if it's flow rate is 0.
                flow_rates_positive = all([valves[name].flow_rate > 0 for name in new_open_valves])
                # Can't open a valve if it's already open.
                previously_opened = len(new_open_valves & open_valves) > 0
                # No point in having two people open the same valve.
                valve_collision = my_choice == el_choice and my_choice == valves[current_rooms[0]]
                if flow_rates_positive and not previously_opened and not valve_collision:
                    max_pressure = max(max_pressure, get_max_released_pressure(tuple(sorted((my_choice.name, el_choice.name))), open_valves | new_open_valves, time_remaining - 1))
                    # released_pressures.append(get_max_released_pressure(tuple(sorted((my_choice.name, el_choice.name))), open_valves | new_open_valves, time_remaining - 1))

    # max_pressure, max_valves = released_pressures[argmax(released_pressures)]
    # return total_flow + max_pressure, max_valves
    # return total_flow + max(released_pressures)
    return total_flow + max_pressure


print("part 1:", get_max_released_pressure(("AA",), frozenset(), 30))
print("part 1:", get_max_released_pressure(("AA","AA"), frozenset(), 26))
# my_pressure, my_valves = get_max_released_pressure(("AA",), frozenset(), 26, frozenset())
# el_pressure, el_valves = get_max_released_pressure(("AA",), frozenset(), 26, my_valves)
# print("part 2:", my_pressure, el_pressure)
