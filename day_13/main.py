"""
--- Day 13: Shuttle Search ---

Your ferry can make it safely to a nearby port, but it won't get much further. When you call to
book another ship, you discover that no ships embark from that port to your vacation island.
You'll need to get from the port to the nearest airport.

Fortunately, a shuttle bus service is available to bring you from the sea port to the airport!
Each bus has an ID number that also indicates how often the bus leaves for the airport.

Bus schedules are defined based on a timestamp that measures the number of minutes since some
fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea
port. After that, each bus travels to the airport, then various other locations, and finally
returns to the sea port to repeat its journey forever.

The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from
the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33,
and so on. If you are there when the bus departs, you can ride that bus to the airport!

Your notes (your puzzle input) consist of two lines. The first line is your estimate of the
earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in
service according to the shuttle company; entries that show x must be out of service,
so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to the
airport. (There will be exactly one such bus.)

For example, suppose you have the following notes:

939
7,13,x,x,59,x,31,19

Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59,
31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:

time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .

The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would
need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of
minutes you'd need to wait gives 295.

What is the ID of the earliest bus you can take to the airport multiplied by the number of
minutes you'll need to wait for that bus?

--- Part Two ---

The shuttle company is running a contest: one gold coin for anyone that can find the earliest
timestamp such that the first bus ID departs at that time and each subsequent listed bus ID
departs at that subsequent minute. (The first line in your input is no longer relevant.)

For example, suppose you have the same list of bus IDs as above:

7,13,x,x,59,x,31,19

An x in the schedule means there are no constraints on what bus IDs must depart at that time.

This means you are looking for the earliest timestamp (called t) such that:

    Bus ID 7 departs at timestamp t.
    Bus ID 13 departs one minute after timestamp t.
    There are no requirements or restrictions on departures at two or three minutes after
        timestamp t.
    Bus ID 59 departs four minutes after timestamp t.
    There are no requirements or restrictions on departures at five minutes after timestamp t.
    Bus ID 31 departs six minutes after timestamp t.
    Bus ID 19 departs seven minutes after timestamp t.

The only bus departures that matter are the listed bus IDs at their specific offsets from t.
Those bus IDs can depart at other times, and other bus IDs can depart at those times. For
example, in the list above, because bus ID 19 must depart seven minutes after the timestamp at
which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes
after timestamp t.

In this example, the earliest timestamp at which this occurs is 1068781:

time     bus 7   bus 13  bus 59  bus 31  bus 19
1068773    .       .       .       .       .
1068774    D       .       .       .       .
1068775    .       .       .       .       .
1068776    .       .       .       .       .
1068777    .       .       .       .       .
1068778    .       .       .       .       .
1068779    .       .       .       .       .
1068780    .       .       .       .       .
1068781    D       .       .       .       .
1068782    .       D       .       .       .
1068783    .       .       .       .       .
1068784    .       .       .       .       .
1068785    .       .       D       .       .
1068786    .       .       .       .       .
1068787    .       .       .       D       .
1068788    D       .       .       .       D
1068789    .       .       .       .       .
1068790    .       .       .       .       .
1068791    .       .       .       .       .
1068792    .       .       .       .       .
1068793    .       .       .       .       .
1068794    .       .       .       .       .
1068795    D       D       .       .       .
1068796    .       .       .       .       .
1068797    .       .       .       .       .

In the above example, bus ID 7 departs at timestamp 1068788 (seven minutes after t). This is
fine; the only requirement on that minute is that bus ID 19 departs then, and it does.

Here are some other examples:

    The earliest timestamp that matches the list 17,x,13,19 is 3417.
    67,7,59,61 first occurs at timestamp 754018.
    67,x,7,59,61 first occurs at timestamp 779210.
    67,7,x,59,61 first occurs at timestamp 1261476.
    1789,37,47,1889 first occurs at timestamp 1202161486.

However, with so many bus IDs in your list, surely the actual earliest timestamp will be larger
than 100000000000000!

What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching
their positions in the list?
"""
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List, Tuple, Union

INPUT_FILE: Path = Path(__file__).parent / "input.txt"
INPUT_STR: List[str] = INPUT_FILE.read_text().split("\n")


def get_timestamp_and_busses(inputs: List[str]) -> Tuple[int, List[int]]:
    timestamp = int(inputs[0])
    busses = [int(element) for element in inputs[1].split(",") if element != "x"]
    return timestamp, busses


def solution_part_1(inputs: List[str]) -> int:
    timestamp, busses = get_timestamp_and_busses(inputs)
    found_bus = False
    departure_time = timestamp
    result = None

    while not found_bus:
        for bus_number in busses:
            # direct multiple of bus number means the bus is leaving at that time
            if departure_time % bus_number == 0:
                found_bus = True
                result = (departure_time - timestamp) * bus_number
        departure_time += 1
    return result


def get_busses_slots(inputs: List[str]) -> List[Union[int, str]]:
    """Get busses for part 2 which needs to include the x values."""
    result = []
    for element in inputs[1].split(","):
        result.append(int(element)) if element != "x" else result.append(element)
    return result


# Everyone says we should use the Chinese remainder theorem, implementation taken from
# https://brilliant.org/wiki/chinese-remainder-theorem/
def chinese_remainder(pairwise_coprime_integer_pairs) -> int:
    total = 0
    N = reduce(mul, [element[1] for element in pairwise_coprime_integer_pairs])
    for x, mx in pairwise_coprime_integer_pairs:
        y_i = N // mx
        total += x * y_i * (y_i ** (mx - 2) % mx)
        total %= N
    return total


def solution_part_2(inputs: List[str]) -> int:
    busses = get_busses_slots(inputs)
    pairs = []
    for index, bus_number in enumerate(busses):
        if bus_number == "x":
            continue
        pairs.append((bus_number - index, bus_number))
    return chinese_remainder(pairwise_coprime_integer_pairs=pairs)


if __name__ == "__main__":
    print(f"Solution for part 1:  {solution_part_1(INPUT_STR)}")
    print(f"Solution for part 2:  {solution_part_2(INPUT_STR)}")
