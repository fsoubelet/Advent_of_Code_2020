"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that
goes directly to the tropical island where you can finally start your vacation. As you reach the
waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area,
you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout
(your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L),
or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly. Fortunately, people are
entirely predictable and always follow a simple set of rules. All decisions are based on the
number of occupied seats adjacent to a given seat (one of the eight positions immediately up,
down, left, right, or diagonal from the seat). The following rules are applied to every seat
simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes
        occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat
    becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further applications of
these rules cause no seats to change state! Once people stop moving around, you count 37 occupied
seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state.
How many seats end up occupied?

--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just care about
adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in
each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied
ones:

.............
.L.L.#.#.#.#.
.............

The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or more visible
occupied seats for an occupied seat to become empty (rather than four or more from the previous
rules). The other rules still apply: empty seats that see no occupied seats become occupied,
seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around
as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once
this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty,
once equilibrium is reached, how many seats end up occupied?
"""
from collections import Counter
from itertools import chain
from pathlib import Path
from typing import List

INPUT_FILE: Path = Path(__file__).parent / "input.txt"
INPUT_PUZZLE: List[str] = INPUT_FILE.read_text().split("\n")


def count_occupied_seats(grid: List[str]) -> int:
    """Return the number of '#' in the grid."""
    return sum([1 for letter in chain.from_iterable(grid) if letter == "#"])


def eval_neighbors(grid: List[str], row_index: int, letter_index: int) -> Counter:
    """Return a count of each value found in the neighors of letter at the provided indices."""
    return Counter(
        grid[row_index + dx][letter_index + dy]
        for dx in range(-1, 2)
        for dy in range(-1, 2)
        if 0 <= row_index + dx < len(grid)
        and 0 <= letter_index + dy < len(grid[row_index])
        and (dx, dy) != (0, 0)
    )


def evolve_grid_part_1(grid: List[str]) -> List[str]:
    """
    Does 1 step evolution of the grid for each position, return the new state of the grid,
    according to the evolving rules of part 1.
    """
    new_grid = list(map(list, grid.copy()))
    for row_index, row in enumerate(grid):
        for letter_index, letter in enumerate(row):
            neighbors_counts = eval_neighbors(grid, row_index, letter_index)
            if letter == "L" and neighbors_counts["#"] == 0:  # empty seat, no occupied adjacent
                new_grid[row_index][letter_index] = "#"  # becomes
            elif letter == "#" and neighbors_counts["#"] >= 4:  # occupied & >=4 occupied adjacent
                new_grid[row_index][letter_index] = "L"  # becomes free
            else:  # any other case, don't change anything
                new_grid[row_index][letter_index] = grid[row_index][letter_index]
    return ["".join(e) for e in new_grid]


def solution_part_1(inputs: List[str]) -> int:  # requires Python 3.8
    grid = inputs.copy()
    while (next_grid := evolve_grid_part_1(grid)) != grid:  # evolve while it changes at each step
        grid = next_grid
    return count_occupied_seats(grid)


def evolve_grid_part_2(grid: List[str]) -> List[str]:
    """
    Does 1 step evolution of the ggrid for each position, return the new state of the ggrid,
    according to the evolving rules of part 2.
    """

    def occupied_neighbors(ggrid: List[str], row_idx: int, letter_idx: int):
        result = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) == (0, 0):
                    continue

                nx = row_idx + dx
                ny = letter_idx + dy
                while 0 <= nx < n and 0 <= ny < m and ggrid[nx][ny] == ".":
                    nx += dx
                    ny += dy

                if (0 <= nx < n) and (0 <= ny < m):
                    result += ggrid[nx][ny] == "#"
        return result

    new_grid = list(map(list, grid.copy()))
    n, m = len(grid), len(grid[0])
    for row_index, row in enumerate(grid):
        for letter_index, letter in enumerate(row):
            occupied = occupied_neighbors(grid, row_index, letter_index)
            if letter == "L" and occupied == 0:
                new_grid[row_index][letter_index] = "#"
            elif letter == "#" and occupied >= 5:
                new_grid[row_index][letter_index] = "L"
            else:
                new_grid[row_index][letter_index] = grid[row_index][letter_index]
    return ["".join(e) for e in new_grid]


def solution_part_2(inputs: List[str]) -> int:  # requires Python 3.8
    grid = inputs.copy()
    while (next_grid := evolve_grid_part_2(grid)) != grid:  # evolve while it changes at each step
        grid = next_grid
    return count_occupied_seats(grid)


if __name__ == "__main__":
    print(f"Solution for part 1:  {solution_part_1(INPUT_PUZZLE)}")
    print(f"Solution for part 2:  {solution_part_2(INPUT_PUZZLE)}")
