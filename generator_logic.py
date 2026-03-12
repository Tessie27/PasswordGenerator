import string
import secrets
import math


SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

COMMON_PASSWORDS = {
    "password", "password1", "123456", "12345678", "qwerty",
    "abc123", "monkey", "1234567", "letmein", "trustno1",
    "dragon", "baseball", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "passw0rd", "shadow", "superman",
    "michael", "football", "password123", "admin", "welcome"
}


def build_character_pool(lowercase=True, uppercase=True, numbers=True, special=True) -> str:
    """Build a character pool based on selected options."""
    pool = ""
    if lowercase:
        pool += string.ascii_lowercase
    if uppercase:
        pool += string.ascii_uppercase
    if numbers:
        pool += string.digits
    if special:
        pool += SPECIAL_CHARS
    return pool


def get_pool_size(lowercase=True, uppercase=True, numbers=True, special=True) -> int:
    """Return the size of the character pool."""
    size = 0
    if lowercase:
        size += 26
    if uppercase:
        size += 26
    if numbers:
        size += 10
    if special:
        size += len(SPECIAL_CHARS)
    return size

def generate_diverse_password(
    length: int,
    lowercase=True, uppercase=True, numbers=True, special=True
) -> str:
    """
    Generate a password that guarantees at least one character
    from each selected character type.
    """
    char_pool = build_character_pool(lowercase, uppercase, numbers, special)

    if not char_pool:
        raise ValueError("At least one character type must be selected.")

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    if length > 127:
        raise ValueError("Password length cannot exceed 127 characters.")

    # Guarantee one of each selected type
    password_chars = []
    if lowercase:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if numbers:
        password_chars.append(secrets.choice(string.digits))
    if special:
        password_chars.append(secrets.choice(SPECIAL_CHARS))

    # Fill remaining length
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(char_pool))

    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)


def calculate_entropy(password: str) -> float:
    """
    Calculate Shannon entropy in bits.
    Formula: L * log2(N)
    where L = password length, N = pool size used.
    """
    if not password:
        return 0.0

    pool_size = 0
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL_CHARS for c in password)

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += len(SPECIAL_CHARS)

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)

def score_password_strength(password: str) -> dict:
    """
    Score password strength and return a detailed result.

    Returns:
        {
            "score": 0-100,
            "label": "Weak" | "Fair" | "Strong" | "Very Strong",
            "entropy": float,
            "is_common": bool,
            "suggestions": [str]
        }
    """
    if not password:
        return {
            "score": 0,
            "label": "Weak",
            "entropy": 0.0,
            "is_common": False,
            "suggestions": ["Enter a password to see its strength."]
        }

    score = 0
    suggestions = []

    # Check if it's a common password
    is_common = password.lower() in COMMON_PASSWORDS
    if is_common:
        return {
            "score": 0,
            "label": "Weak",
            "entropy": calculate_entropy(password),
            "is_common": True,
            "suggestions": ["This is a very common password. Please choose something unique!"]
        }

    # Length scoring (up to 40 points)
    length = len(password)
    if length >= 8:
        score += 10
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    if length >= 20:
        score += 10
    else:
        suggestions.append("Use 20+ characters for maximum security.")

    # Character variety (up to 40 points)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL_CHARS for c in password)

    if has_lower:
        score += 10
    else:
        suggestions.append("Add lowercase letters.")

    if has_upper:
        score += 10
    else:
        suggestions.append("Add uppercase letters.")

    if has_digit:
        score += 10
    else:
        suggestions.append("Add numbers.")

    if has_special:
        score += 10
    else:
        suggestions.append("Add special characters like !@#$.")

    # Entropy bonus (up to 20 points)
    entropy = calculate_entropy(password)
    if entropy >= 60:
        score += 10
    if entropy >= 80:
        score += 10
    elif entropy < 40:
        suggestions.append("Increase length or use more character types.")

    # Determine label
    if score >= 80:
        label = "Very Strong"
    elif score >= 60:
        label = "Strong"
    elif score >= 40:
        label = "Fair"
    else:
        label = "Weak"

    return {
        "score": score,
        "label": label,
        "entropy": round(entropy, 1),
        "is_common": False,
        "suggestions": suggestions
    }


def validate_custom_password(password: str) -> tuple:
    """
    Validate a custom password.
    Returns (is_valid: bool, reason: str)
    """
    if not password or not password.strip():
        return False, "empty"
    if len(password) < 8:
        return False, "too_short"
    if len(password) > 127:
        return False, "too_long"
    return True, "ok"