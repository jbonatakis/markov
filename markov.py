import random
import sys
from typing import Dict


def next_letter_counts() -> Dict:
    letters = {}

    with open("names.male.txt", "r") as txt:
        names = [line.rstrip("\n") for line in txt]

    for name in names:
        name = name.lower()

        for i in range(len(name)):
            try:
                letter = name[i]
                next = name[i + 1]
            except IndexError:
                continue

            if letter not in letters:
                letters[letter] = {next: 1}
            else:
                if next not in letters[letter]:
                    letters[letter][next] = 1
                else:
                    letters[letter][next] += 1

    return letters


def generate_probabilities(letters: Dict[str, Dict[str, int]]) -> Dict:
    """
    Rather than sorting:
    * Sum within a number
    * Update each value in place
    """
    for _, counts in letters.items():
        letter_sum = 0
        for letter, cnt in counts.items():
            letter_sum += cnt

        for letter, cnt in counts.items():
            counts[letter] = cnt / letter_sum

    return letters


def select_letter(outer_map, key):
    inner_map = outer_map[key]

    # Create a list of cumulative probabilities and corresponding letters
    cumulative_distribution = []
    cumulative_prob = 0.0

    for letter, probability in inner_map.items():
        cumulative_prob += probability
        cumulative_distribution.append((cumulative_prob, letter))

    # Generate a random number between 0 and 1
    random_number = random.random()

    # Find the letter corresponding to the random number
    for cumulative_prob, letter in cumulative_distribution:
        if random_number < cumulative_prob:
            return letter

    # In case of rounding errors, return the last letter
    return cumulative_distribution[-1][1]


def generate_word(probabilities, length: int, starts_with: str) -> str:
    word = starts_with
    for _ in range(length):
        word += select_letter(probabilities, word[-1])
    return word.capitalize()


def main():
    import time

    letters = next_letter_counts()
    probabilities = generate_probabilities(letters)

    try:
        number_of_words = int(sys.argv[2])
    except (IndexError, ValueError):
        number_of_words = 10

    start = time.time()
    for _ in range(number_of_words):
        word = generate_word(probabilities, random.randint(4, 8), sys.argv[1].lower())
        print(word)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
