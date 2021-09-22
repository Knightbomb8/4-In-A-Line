from board import Board


# gets a string input from a user in python
def get_string_input(message, string_options):
    while(True):
        # attempts to receive a string from the user of a certain type
        try:
            string = input(message)

            if string in string_options:
                return string
            else:
                print("Invalid entry")

        except:
            print("Invalid entry")
