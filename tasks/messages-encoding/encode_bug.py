def encode_string(input_string):
    capital_dict = {
    'A': '@', 'B': '#', 'C': '$', 'D': '%', 'E': '&', 'F': '*', 'G': '^',
    'H': '(', 'I': ')', 'J': '+', 'K': '=', 'L': '|', 'M': '{', 'N': '}',
    'O': '[', 'P': ']', 'Q': ':', 'R': ';', 'S': ',', 'T': '.', 'U': '?',
    'V': '<', 'W': '>', 'X': '!', 'Y': '_', 'Z': '/'
}

    encoded_string = ''
    for char in input_string:
        if char.isupper():
            encoded_string += capital_dict[char]
        elif char.islower():
            encoded_string += capital_dict[char] * 2

    for char in input_string:
        if char.isdigit():
            num = int(char)
            encoded_string += str(num + 1)
            

    symbol_replace_dict = {
    '!': 'A', '@': 'B', '#': 'C', '$': 'D', '%': 'E', '^': 'F',
    '&': 'G', '*': 'H', '(': 'I', ')': 'J', '-': 'K', '_': 'L',
    '=': 'M', '+': 'N', '[': 'O', ']': 'P', '{': 'Q', '}': 'R',
    '|': 'S', '\\': 'T', ';': 'U', ':': 'V', "'": 'W', '"': 'X',
    ',': 'Y', '.': 'Z', '<': 'a', '>': 'b', '/': 'c', '?': 'd'
}

    for char in input_string:
        if char in symbol_replace_dict:
            encoded_string += symbol_replace_dict[char]

    return encoded_string


def encode_multiple_rounds(input_string):
    encoded_string = encode_string(input_string)
    encoded_string = encoded_string[::-1]
    return encoded_string

def decode_string(encoded_string):
    pass


def show_menu():
    """Display interactive menu"""
    print("SECURE MESSAGE ENCODING SYSTEM")
    print("\n 1. Encode a message")
    print("\n 2. Decode a message") 
    print("\n 3. Exit")
def main():
    """Main interactive function"""

        
    while True:
        show_menu()
        choice = input("\nSelect option (1-3):").strip()
        
        if choice == '1':
            input_text = input("Enter text to encode: ").strip()
            if input_text:
                encoded = encode_multiple_rounds(input_text)
                print(f"Encoded result: {encoded}")
        elif choice == '2':
            input_text = input("Enter text to decode: ").strip()
            if input_text:
                decoded = decode_string(input_text)
                print(f"Decoded result: {decoded}")
        elif choice == '3':
            print("Thank you for using the Secure Message Encoding System!")
            break
        else:
            print("Invalid choice. Please select 1-3.")
            continue
        


if __name__ == "__main__":
    main()