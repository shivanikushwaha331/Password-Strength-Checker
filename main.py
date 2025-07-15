#### Check for length and character types
import string
import re

def check_length(password):
    return len(password)

def check_char_types(password):
    has_upper = any(a.isupper() for a in password)
    has_lower = any(a.islower() for a in password)
    has_digit = any(a.isdigit() for a in password)
    has_special = any(a in string.punctuation for a in password)
    return has_upper, has_lower, has_digit, has_special

#### Load common password list

def load_common_passwords(file_path="Passwordlist.txt"):
    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
        return set(line.strip() for line in f)

### Detect Simple Patterns
def detect_patterns(password):
    patterns = ["1234", "qwerty", "password", "abc", "111", "0000"]
    for pattern in patterns:
        if pattern in password.lower():
            return True
    if re.search(r'(..+)\1', password):  # repeated substrings
        return True
    return False

## Create Scoring Logic
def score_password(password, common_passwords):
    score = 0
    length = check_length(password)
    has_upper, has_lower, has_digit, has_special = check_char_types(password)
    pattern_found = detect_patterns(password)

    # Length points
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Character diversity
    score += sum([has_upper, has_lower, has_digit, has_special])

    # Penalty for patterns or common password
    if pattern_found or password in common_passwords:
        score -= 2

    # Bound the score
    score = max(0, min(score, 6))

    # Strength level
    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return {
        "score": score,
        "strength": strength,
        "length": length,
        "char_types": {
            "uppercase": has_upper,
            "lowercase": has_lower,
            "digits": has_digit,
            "specials": has_special
        },
        "pattern_found": pattern_found
    }

##  Main Program (CLI)
def main():
    common_passwords = load_common_passwords()
    pwd = input("Enter password to check strength: ")

    result = score_password(pwd, common_passwords)

    print(f"\nPassword Strength: {result['strength']}")
    print(f"Score: {result['score']} / 6")
    print(f"Length: {result['length']}")
    print("Character Types Used:")
    for k, v in result['char_types'].items():
        print(f"  {k.capitalize()}: {'Yes' if v else 'No'}")
    print("Pattern Detected:", "Yes" if result['pattern_found'] else "No")

if __name__ == "__main__":
    main()
