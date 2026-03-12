import pytest
import string
import secrets

# ─── Test the core logic WITHOUT needing PyQt5 or GUI ──────────────

# Copy the pure logic functions here so we can test them without GUI
SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

def build_character_pool(lowercase=True, uppercase=True, numbers=True, special=True):
    char_pool = ""
    if lowercase:
        char_pool += string.ascii_lowercase
    if uppercase:
        char_pool += string.ascii_uppercase
    if numbers:
        char_pool += string.digits
    if special:
        char_pool += SPECIAL_CHARS
    return char_pool

def generate_diverse_password(char_pool, length, lowercase=True, uppercase=True, numbers=True, special=True):
    password_chars = []
    if lowercase:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if numbers:
        password_chars.append(secrets.choice(string.digits))
    if special:
        password_chars.append(secrets.choice(SPECIAL_CHARS))
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(char_pool))
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

# ─── Character Pool Tests ──────────────────────────────────────────

def test_pool_all_options():
    """All options enabled should include all character types"""
    pool = build_character_pool()
    assert any(c in string.ascii_lowercase for c in pool)
    assert any(c in string.ascii_uppercase for c in pool)
    assert any(c in string.digits for c in pool)
    assert any(c in SPECIAL_CHARS for c in pool)

def test_pool_lowercase_only():
    """Only lowercase selected should only have lowercase"""
    pool = build_character_pool(uppercase=False, numbers=False, special=False)
    assert pool == string.ascii_lowercase

def test_pool_uppercase_only():
    pool = build_character_pool(lowercase=False, numbers=False, special=False)
    assert pool == string.ascii_uppercase

def test_pool_numbers_only():
    pool = build_character_pool(lowercase=False, uppercase=False, special=False)
    assert pool == string.digits

def test_pool_empty_when_nothing_selected():
    """No options selected should return empty pool"""
    pool = build_character_pool(lowercase=False, uppercase=False, numbers=False, special=False)
    assert pool == ""

# ─── Password Generation Tests ─────────────────────────────────────

def test_password_correct_length():
    """Generated password must match requested length"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 16)
    assert len(password) == 16

def test_password_min_length():
    """Minimum length password (8 chars) should work"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 8)
    assert len(password) == 8

def test_password_max_length():
    """Maximum length password (127 chars) should work"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 127)
    assert len(password) == 127

def test_password_has_uppercase():
    """Password should contain at least one uppercase letter"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 16)
    assert any(c.isupper() for c in password)

def test_password_has_lowercase():
    """Password should contain at least one lowercase letter"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 16)
    assert any(c.islower() for c in password)

def test_password_has_digit():
    """Password should contain at least one digit"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 16)
    assert any(c.isdigit() for c in password)

def test_password_has_special():
    """Password should contain at least one special character"""
    pool = build_character_pool()
    password = generate_diverse_password(pool, 16)
    assert any(c in SPECIAL_CHARS for c in password)

def test_passwords_are_unique():
    """Two generated passwords should not be identical"""
    pool = build_character_pool()
    p1 = generate_diverse_password(pool, 16)
    p2 = generate_diverse_password(pool, 16)
    assert p1 != p2

def test_password_only_uses_pool_chars():
    """Password should only contain characters from the pool"""
    pool = build_character_pool(special=False)
    password = generate_diverse_password(pool, 16, special=False)
    for char in password:
        assert char in pool

# ─── WordManager Tests ─────────────────────────────────────────────

def test_word_manager_missing_file():
    """WordManager should raise FileNotFoundError if words.txt missing"""
    from word_manager import WordManager
    with pytest.raises(FileNotFoundError):
        WordManager(word_file="nonexistent_file.txt")

def test_word_manager_loads_words(tmp_path):
    """WordManager should load words correctly from a valid file"""
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\ncherry\norange\ngrape\n")
    wm = WordManager(word_file=str(word_file))
    assert wm.get_word_count() == 5

def test_get_random_words(tmp_path):
    """Should return the correct number of random words"""
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\ncherry\norange\ngrape\n")
    wm = WordManager(word_file=str(word_file))
    words = wm.get_random_words(3)
    assert len(words) == 3

def test_get_random_words_are_from_list(tmp_path):
    """Returned words should all come from the word list"""
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\ncherry\norange\ngrape\n")
    wm = WordManager(word_file=str(word_file))
    words = wm.get_random_words(3)
    for word in words:
        assert word in ["apple", "banana", "cherry", "orange", "grape"]

def test_get_too_many_words_raises(tmp_path):
    """Asking for more words than available should raise Exception"""
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\n")
    wm = WordManager(word_file=str(word_file))
    with pytest.raises(Exception):
        wm.get_random_words(10)

# ─── Custom Password Validation Tests ──────────────────────────────

def validate_custom_password(password):
    """Mirrors the validation logic in use_custom_password()"""
    if not password:
        return False, "empty"
    if len(password) < 8:
        return False, "too_short"
    if len(password) > 127:
        return False, "too_long"
    return True, "ok"

def test_custom_password_valid():
    valid, reason = validate_custom_password("MyP@ssw0rd")
    assert valid == True

def test_custom_password_too_short():
    valid, reason = validate_custom_password("abc")
    assert valid == False
    assert reason == "too_short"

def test_custom_password_too_long():
    valid, reason = validate_custom_password("a" * 128)
    assert valid == False
    assert reason == "too_long"

def test_custom_password_empty():
    valid, reason = validate_custom_password("")
    assert valid == False
    assert reason == "empty"