import random
import sys
import numpy as np

np.set_printoptions(threshold = sys.maxsize)

available_characters = "abcdefghijklmnopqrstuvwxyz0123456789,.?;- "
matrix_size = len(available_characters)

iterations = 0
occurences = np.matrix([
    [0.0 for j in range(matrix_size)] for i in range(matrix_size)
])

def getMatrixIndex(char):
    return available_characters.index(char)
def setCharOutcome(char, out):
    index = getMatrixIndex(char)
    index_out = getMatrixIndex(out)
    position = (index, index_out)
    occurences.itemset(position, occurences.item(position) + 1)

def loadData(text):
    global iterations
    filtered_text = text.lower()

    prev = None
    for char in filtered_text:
        if char in available_characters: # if char is one of the available characters
            if not prev: # if prev doesn't exist
                prev = char
                continue
            setCharOutcome(prev, char)
            prev = char

    for i in range(matrix_size):
        row_sum = occurences.sum(1).item((i, 0))
        for j in range(matrix_size):
            position = (i, j)
            new_value = 0
            if row_sum != 0:
                new_value = occurences.item(position) / row_sum

            # print(f"ttt {new_value} {occurences.item(position)} / {row_sum}")
            occurences.itemset(position, new_value)
            # print(f"{new_value} : {occurences.item(position)}")

def randomNext(transition_matrix, char):
    rand = random.random()
    index = getMatrixIndex(char)

    probability = 0
    for i in range(matrix_size):
        position = (index, i)
        probability += transition_matrix.item(position)
        # print(f"probability {probability} {transition_matrix.item(position)}/{row_sum}")
        # print(f" - {available_characters[i]}")

        if rand <= probability:
            return available_characters[i]
    return None

def generate(starting_text, max_chars):
    transition_matrix = occurences.copy()

    filtered_starting_text = ""
    for char in starting_text.lower():
        if char in available_characters:
            filtered_starting_text += char

    output = starting_text
    starting_char = starting_text[-1]

    prev = starting_char
    for i in range(max_chars):
        _next = randomNext(transition_matrix, prev)
        # print(f"p {_next}")
        if not _next: # If there's nothing left to generate, break
            break
        prev = _next
        output += _next

        # transition_matrix = np.matmul(transition_matrix, occurences)
    return output

print("Loading data...")
loadData(open("training_data.txt", "r").read())

print("Enter your prompt here:")
print(generate(input(), 1000))