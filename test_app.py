import pytest
import string
import math
from generator_logic import (
    build_character_pool,
    get_pool_size,
    generate_diverse_password,
    calculate_entropy,
    score_password_strength,
    validate_custom_password,
    SPECIAL_CHARS,
    COMMON_PASSWORDS,
)


def test_pool_all_options():
    pool = build_character_pool()
    assert any(c in string.ascii_lowercase for c in pool)
    assert any(c in string.ascii_uppercase for c in pool)
    assert any(c in string.digits for c in pool)
    assert any(c in SPECIAL_CHARS for c in pool)

def test_pool_lowercase_only():
    pool = build_character_pool(uppercase=False, numbers=False, special=False)
    assert pool == string.ascii_lowercase

def test_pool_uppercase_only():
    pool = build_character_pool(lowercase=False, numbers=False, special=False)
    assert pool == string.ascii_uppercase

def test_pool_numbers_only():
    pool = build_character_pool(lowercase=False, uppercase=False, special=False)
    assert pool == string.digits

def test_pool_empty_when_nothing_selected():
    pool = build_character_pool(lowercase=False, uppercase=False, numbers=False, special=False)
    assert pool == ""

def test_pool_size_all():
    size = get_pool_size()
    assert size == 26 + 26 + 10 + len(SPECIAL_CHARS)

def test_pool_size_lowercase_only():
    assert get_pool_size(uppercase=False, numbers=False, special=False) == 26

def test_password_correct_length():
    password = generate_diverse_password(16)
    assert len(password) == 16

def test_password_min_length():
    password = generate_diverse_password(8)
    assert len(password) == 8

def test_password_max_length():
    password = generate_diverse_password(127)
    assert len(password) == 127

def test_password_has_uppercase():
    password = generate_diverse_password(16)
    assert any(c.isupper() for c in password)

def test_password_has_lowercase():
    password = generate_diverse_password(16)
    assert any(c.islower() for c in password)

def test_password_has_digit():
    password = generate_diverse_password(16)
    assert any(c.isdigit() for c in password)

def test_password_has_special():
    password = generate_diverse_password(16)
    assert any(c in SPECIAL_CHARS for c in password)

def test_passwords_are_unique():
    p1 = generate_diverse_password(16)
    p2 = generate_diverse_password(16)
    assert p1 != p2

def test_password_raises_on_empty_pool():
    with pytest.raises(ValueError, match="At least one"):
        generate_diverse_password(16, lowercase=False, uppercase=False, numbers=False, special=False)

def test_password_raises_on_too_short():
    with pytest.raises(ValueError, match="at least 8"):
        generate_diverse_password(4)

def test_password_raises_on_too_long():
    with pytest.raises(ValueError, match="cannot exceed 127"):
        generate_diverse_password(200)

def test_password_only_uses_selected_chars():
    pool = build_character_pool(special=False)
    password = generate_diverse_password(20, special=False)
    for char in password:
        assert char in pool, f"Unexpected char '{char}' not in pool"


def test_entropy_is_positive():
    entropy = calculate_entropy("MyP@ssw0rd!")
    assert entropy > 0

def test_entropy_increases_with_length():
    short = calculate_entropy("Ab1!")
    long = calculate_entropy("Ab1!Ab1!Ab1!Ab1!")
    assert long > short

def test_entropy_increases_with_variety():
    simple = calculate_entropy("aaaaaaaaaaaaaaaa")   # only lowercase
    complex_ = calculate_entropy("Aa1!Aa1!Aa1!Aa1!")  # all types
    assert complex_ > simple

def test_entropy_empty_password():
    assert calculate_entropy("") == 0.0

def test_entropy_formula():
    """Verify entropy matches L * log2(N) for a known pool."""
    # lowercase only password
    password = "abcdefghijklmnop"  # 16 chars, lowercase only
    expected = 16 * math.log2(26)
    assert abs(calculate_entropy(password) - expected) < 0.01


def test_strength_weak_short_password():
    result = score_password_strength("abc")
    assert result["label"] == "Weak"
    assert result["score"] < 40

def test_strength_common_password():
    result = score_password_strength("password")
    assert result["is_common"] == True
    assert result["score"] == 0
    assert result["label"] == "Weak"

def test_strength_strong_password():
    result = score_password_strength("Tr0ub4dor&3XyZ!")
    assert result["label"] in ["Strong", "Very Strong"]
    assert result["score"] >= 60

def test_strength_very_strong_password():
    result = score_password_strength("X9#mK!pL2@nQ8$wR5^vT")
    assert result["label"] == "Very Strong"
    assert result["score"] >= 80

def test_strength_returns_entropy():
    result = score_password_strength("MyP@ssw0rd123!")
    assert result["entropy"] > 0

def test_strength_suggestions_for_weak():
    result = score_password_strength("alllowercase")
    assert len(result["suggestions"]) > 0

def test_strength_no_suggestions_for_very_strong():
    result = score_password_strength("X9#mK!pL2@nQ8$wR5^vT1&")
    assert result["label"] == "Very Strong"

def test_strength_empty_password():
    result = score_password_strength("")
    assert result["score"] == 0
    assert result["label"] == "Weak"

def test_common_passwords_list_not_empty():
    assert len(COMMON_PASSWORDS) > 0

def test_common_passwords_contains_known():
    assert "password" in COMMON_PASSWORDS
    assert "123456" in COMMON_PASSWORDS


def test_custom_password_valid():
    valid, reason = validate_custom_password("MyP@ssw0rd")
    assert valid == True
    assert reason == "ok"

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

def test_custom_password_whitespace_only():
    valid, reason = validate_custom_password("     ")
    assert valid == False
    assert reason == "empty"

def test_custom_password_exactly_8_chars():
    valid, reason = validate_custom_password("Abcd1234")
    assert valid == True

def test_custom_password_exactly_127_chars():
    valid, reason = validate_custom_password("a" * 127)
    assert valid == True

def test_word_manager_missing_file():
    from word_manager import WordManager
    with pytest.raises(FileNotFoundError):
        WordManager(word_file="nonexistent_file.txt")

def test_word_manager_loads_words(tmp_path):
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\ncherry\norange\ngrape\n")
    wm = WordManager(word_file=str(word_file))
    assert wm.get_word_count() == 5

def test_get_random_words(tmp_path):
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\ncherry\norange\ngrape\n")
    wm = WordManager(word_file=str(word_file))
    words = wm.get_random_words(3)
    assert len(words) == 3

def test_get_random_words_from_list(tmp_path):
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_list = ["apple", "banana", "cherry", "orange", "grape"]
    word_file.write_text("\n".join(word_list))
    wm = WordManager(word_file=str(word_file))
    for word in wm.get_random_words(3):
        assert word in word_list

def test_get_too_many_words_raises(tmp_path):
    from word_manager import WordManager
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple\nbanana\n")
    wm = WordManager(word_file=str(word_file))
    with pytest.raises(Exception):
        wm.get_random_words(10)