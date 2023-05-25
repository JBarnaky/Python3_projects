while True:
    print("Options:")
    print("Enter, 'add' to add two numbers")
    print("Enter, 'sub' to subtract two numbers")
    print("Enter, 'mult' to multiply two numbers")
    print("Enter, 'div' to divide two numbers")
    print("Enter, 'quit' to exit the program")
    user_input = input(": ")

    if user_input == "quit":
        print("Exiting program. Goodbye!")
        break
    elif user_input in ["add", "sub", "mult", "div"]:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if user_input == "add":
            result = num1 + num2
        elif user_input == "sub":
            result = num1 - num2
        elif user_input == "mult":
            result = num1 * num2
        else:
            if num2 != 0:
                result = num1 / num2
            else:
                print("Error: division by zero")
                continue

        print(f"The result of {user_input} is {result}")
        input("Press enter to continue")
    else:
        print("Unknown input. Please try again.") 
