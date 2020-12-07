"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks like you'll even
have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags
and their contents; bags must be color-coded and must contain specific quantities of other
color-coded bags. Apparently, nobody responsible for these regulations considered how long they
would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example, every faded blue bag
is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many
different bag colors would be valid for the outermost bag? (In other words: how many colors can,
eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

    A bright white bag, which can hold your shiny gold bag directly.
    A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
    A dark orange bag, which can hold bright white and muted yellow bags, either of which could
        then hold your shiny gold bag.
    A light red bag, which can hold bright white and muted yellow bags, either of which could
        then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually contain at least one shiny gold
bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is
quite long; make sure you get all of it.)

--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices, but because of
the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2
vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example;
be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""
from pathlib import Path
from typing import List

INPUT_FILE: Path = Path(__file__).parent / "input.txt"
INPUT_LINES: List[str] = INPUT_FILE.read_text().split("\n")


def check_bag(bag_rules: dict, checked_bag: str, current_bag: str):
    if current_bag == checked_bag:
        return 1
    if not bag_rules.get(current_bag):
        return 0
    else:
        counts = []
        for k, v in bag_rules[current_bag].items():
            counts.append(check_bag(bag_rules, checked_bag, k))
        return max(counts)


def get_bag_rules(inputs: List[str]) -> dict:
    """
    Return a dictionnary with different bags as keys and as values a dictionnary of their rule
    content (bags as keys, amount as values), recursively collected.
    """
    bag_names = []
    all_rules = {}
    for line in inputs:
        bag = " ".join(line.split(" ")[:2])
        contents = line[line.index("contain") + 8 : -1].split(",")  # all after 'contains'
        contents = [cnt.lstrip() for cnt in contents]  # get them in a list
        contents = [" ".join(cont.split(" ")[:-1]) for cont in contents]  # remove 'bags' for each
        contents = {
            " ".join(cont.split(" ")[1:]): cont.split(" ")[0] for cont in contents
        }  # get {bad: quantity} for each of these bags

        if bag not in bag_names:
            bag_names.append(bag)
        if all_rules.get(bag):
            contents.update(all_rules[bag])
        all_rules[bag] = contents

    for bag, rules in all_rules.items():
        if rules == {"other": "no"}:  # replace empty bad contents from {'other': 'no'} to {}
            all_rules[bag] = {}
    for bag, rules in all_rules.items():
        all_rules[bag] = {k: int(v) for k, v in rules.items()}  # convert values to int
    return all_rules


def solution_part_1(inputs: List[str]) -> int:
    possible_bags = 0
    bag_rules: dict = get_bag_rules(inputs)
    for bag, _ in bag_rules.items():
        if bag != "shiny gold":
            possible_bags += check_bag(bag_rules, "shiny gold", bag)
    return possible_bags


def solution_part_2(inputs: List[str]) -> int:
    result = 0
    bag_rules: dict = get_bag_rules(inputs)

    def add_colors(rules: dict, color: str) -> int:
        total = 0
        for other_color, quantity in rules[color].items():
            total += quantity * (1 + add_colors(rules, other_color))
        return total

    return add_colors(rules=bag_rules, color="shiny gold")


if __name__ == "__main__":
    print(f"Solution for part 1:  {solution_part_1(INPUT_LINES)}")
    print(f"Solution for part 2:  {solution_part_2(INPUT_LINES)}")
