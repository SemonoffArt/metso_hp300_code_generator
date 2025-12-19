"""Core calculation logic for METSO HP300 code generator.

This module implements the real engineering/service code algorithm
as described in the project documentation.
"""


def _compute_key_code(unlock_code: int) -> int:
    """Compute raw service key code from an integer unlock code."""
    key_code = (unlock_code & 3) << 14
    key_code += (unlock_code & 60) << 4
    key_code += (unlock_code & 960) << 4
    key_code += (unlock_code & 15360) >> 8
    key_code += (49152 & unlock_code) >> 14
    key_code ^= 43605
    return key_code


def _format_key_code(key_code: int) -> str:
    """Format key code as a 4+ digit hexadecimal string with message."""
    if key_code > 4095:
        hex_part = f"{key_code:X}"
    elif key_code >= 256:
        hex_part = f"0{key_code:X}"
    elif key_code >= 16:
        hex_part = f"00{key_code:X}"
    else:
        hex_part = f"000{key_code:X}"
    return f"{hex_part} is valid key code"


def calculate_engineering_code(input_code: str) -> str:
    """Calculate engineering/service code string from a hex unlock code.

    Expects a 4-character hexadecimal string. Input validation (length,
    allowed characters) is handled at a higher level; this function
    assumes valid hexadecimal input and may raise ValueError if parsing
    fails.
    """
    unlock_code = int(input_code, 16)
    key_code = _compute_key_code(unlock_code)
    return _format_key_code(key_code)
