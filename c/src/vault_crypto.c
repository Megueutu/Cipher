#include "vault_crypto.h"

const char *vault_crypto_status_message(vault_crypto_status status) {
    switch (status) {
        case VAULT_CRYPTO_OK: return "ok";
        case VAULT_CRYPTO_INVALID_ARGUMENT: return "invalid argument";
        case VAULT_CRYPTO_BUFFER_TOO_SMALL: return "output buffer too small";
        case VAULT_CRYPTO_AUTH_FAILED: return "authentication failed";
        case VAULT_CRYPTO_NOT_IMPLEMENTED: return "not implemented";
        default: return "unknown status";
    }
}

void vault_crypto_secure_zero(void *buffer, size_t length) {
    volatile uint8_t *bytes = buffer;

    while (bytes != NULL && length-- > 0U) {
        *bytes++ = 0U;
    }
}

vault_crypto_status vault_crypto_derive_key(
    const uint8_t *master_password,
    size_t master_password_length,
    const uint8_t salt[VAULT_CRYPTO_SALT_BYTES],
    uint8_t key[VAULT_CRYPTO_KEY_BYTES]
) {
    if (master_password == NULL || master_password_length == 0U || salt == NULL || key == NULL) {
        return VAULT_CRYPTO_INVALID_ARGUMENT;
    }

    /* TODO: replace with crypto_pwhash(..., crypto_pwhash_ALG_ARGON2ID13). */
    return VAULT_CRYPTO_NOT_IMPLEMENTED;
}

vault_crypto_status vault_crypto_encrypt(
    const uint8_t key[VAULT_CRYPTO_KEY_BYTES],
    const uint8_t nonce[VAULT_CRYPTO_NONCE_BYTES],
    const uint8_t *associated_data,
    size_t associated_data_length,
    const uint8_t *plaintext,
    size_t plaintext_length,
    uint8_t *ciphertext,
    size_t ciphertext_capacity,
    size_t *ciphertext_length
) {
    if (key == NULL || nonce == NULL || plaintext == NULL || ciphertext == NULL || ciphertext_length == NULL ||
        (associated_data == NULL && associated_data_length != 0U)) {
        return VAULT_CRYPTO_INVALID_ARGUMENT;
    }
    if (ciphertext_capacity < plaintext_length + VAULT_CRYPTO_TAG_BYTES) {
        return VAULT_CRYPTO_BUFFER_TOO_SMALL;
    }

    /* TODO: replace with crypto_aead_xchacha20poly1305_ietf_encrypt. */
    return VAULT_CRYPTO_NOT_IMPLEMENTED;
}

vault_crypto_status vault_crypto_decrypt(
    const uint8_t key[VAULT_CRYPTO_KEY_BYTES],
    const uint8_t nonce[VAULT_CRYPTO_NONCE_BYTES],
    const uint8_t *associated_data,
    size_t associated_data_length,
    const uint8_t *ciphertext,
    size_t ciphertext_length,
    uint8_t *plaintext,
    size_t plaintext_capacity,
    size_t *plaintext_length
) {
    if (key == NULL || nonce == NULL || ciphertext == NULL || plaintext == NULL || plaintext_length == NULL ||
        (associated_data == NULL && associated_data_length != 0U)) {
        return VAULT_CRYPTO_INVALID_ARGUMENT;
    }
    if (ciphertext_length < VAULT_CRYPTO_TAG_BYTES || plaintext_capacity < ciphertext_length - VAULT_CRYPTO_TAG_BYTES) {
        return VAULT_CRYPTO_BUFFER_TOO_SMALL;
    }

    /* TODO: replace with crypto_aead_xchacha20poly1305_ietf_decrypt. */
    return VAULT_CRYPTO_NOT_IMPLEMENTED;
}
