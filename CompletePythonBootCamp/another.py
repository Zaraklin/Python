import name_and_main

print("another.py")

name_and_main.func

if __name__ == "__main__":
    print("another.py is being run directly!")
else:
    print("another.py has been imported!")