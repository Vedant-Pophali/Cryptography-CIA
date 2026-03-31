# 5-Bit Masked Autokey Cipher

An enhanced **Autokey Cipher** utilizing bitwise XOR operations within a 5-bit ($2^5 = 32$) character space. This implementation functions as a self-synchronizing stream cipher with dual-layer defense.

## Core Workflow

1.  **Salt Generation**: Sums the ASCII values of the **Master Password** (modulo 32) to generate a 5-bit mask.
2.  **Keystream Logic**: Starts with a secret **Primer**. Post-initialization, the plaintext is appended to the primer to create a continuous, non-repeating keystream.
3.  **Masking Layer**: The raw key is XORed with the salt ($Key \oplus Salt$) to hide plaintext feedback and prevent "sliding window" attacks.
4.  **Transformation**:
    *   **Encryption**: $Plaintext \oplus MaskedKey$
    *   **Decryption**: $Ciphertext \oplus MaskedKey$ (Recovered text is fed back to sustain the stream).


## Constraints & Mapping

*   **Dictionary**: 32 characters: `A–Z` (0–25) and `1–6` (26–31).
*   **Case Sensitivity**: Strict **UPPERCASE** only.
*   **Whitespace**: Preserved visually but ignored by encryption logic to maintain key alignment.
*   **Unsupported**: Special characters, punctuation, and digits `0`, `7`, `8`, and `9`.


## Security & Risks

*   **Layered Defense**: Combines a **Structural Key** (Primer) and a **Masking Key** (Master Password) to resist frequency analysis.
*   **Null-Masking Risk**: If the password sum is a multiple of 32, the salt becomes 0, leaving the raw key exposed ($X \oplus 0 = X$).
