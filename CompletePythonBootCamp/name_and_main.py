def func():
    print("1 func()")

print("Top level in name_and_main.py")

if __name__ == "__main__":
    print("name_and_main.py is being run directly!")
else:
    print("name_and_main.py has been imported!")