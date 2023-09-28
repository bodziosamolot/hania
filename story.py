import keyboard

welcome = "stoisz przed domem"
print(welcome)
print("przyciśnij 1 aby wejść do środka, 2 aby zostać na dworze")

key = keyboard.read_key()

if key == "1":
    print("Jestes w przedpokoju")
if key