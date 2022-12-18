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

@lru_cache(maxsize=None)
def get_max_released_pressure(current_room: str, open_valves: frozenset, time_remaining: int):
    if time_remaining == 0:
        return 0

    total_flow = sum([valves[name].flow_rate for name in open_valves])
    released_pressures = []
    # Try to open the valve in the current room
    if current_room not in open_valves:
        released_pressures.append(get_max_released_pressure(current_room, open_valves | {current_room}, time_remaining - 1))

    for n in valves[current_room].neighbors:
        released_pressures.append(get_max_released_pressure(n.name, open_valves, time_remaining - 1))

    print("Line 47", current_room, open_valves, time_remaining, total_flow + max(released_pressures))
    return total_flow + max(released_pressures)


print("max_released_pressure", get_max_released_pressure("AA", frozenset(), 30))
