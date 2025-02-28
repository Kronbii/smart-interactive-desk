import sys

def main():
    # Read the action passed from Node.js via stdin
    action = sys.stdin.readline().strip()
    
    # Process the action (you can add more processing logic here)
    print(f"Python received action: {action}")
    
    """
    # Example: respond back with a processed message
    response = f"Processed action: {action}"
    
    # Output the response to stdout
    print(response)
    """

if __name__ == "__main__":
    main()
