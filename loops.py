word = "deleveled"

wordLength = len(word)

reverse = ""

for number in range(wordLength - 1, -1, -1):
    reverse = reverse + word[number]

print(word == reverse)
