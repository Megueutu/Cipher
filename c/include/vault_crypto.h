#ifndef VAULT_CRYPTO_H
#define VAULT_CRYPTO_H

#include <stddef.h>
#include <stdint.h>

#if defined(_WIN32)
#if defined(VAULT_CRYPTO_BUILD)
#define VAULT_CRYPTO_API __declspec(dllexport)
#else
#define VAULT_CRYPTO_API __declspec(dllimport)
#endif
#else
#define VAULT_CRYPTO_API
#endif

#define VAULT_CRYPTO_SALT_BYTES 16U
#define VAULT_CRYPTO_NONCE_BYTES 24U
#define VAULT_CRYPTO_KEY_BYTES 32U
#define VAULT_CRYPTO_TAG_BYTES 16U

typedef enum {
    VAULT_CRYPTO_OK = 0,
    VAULT_CRYPTO_INVALID_ARGUMENT = 1,
    VAULT_CRYPTO_BUFFER_TOO_SMALL = 2,
    VAULT_CRYPTO_AUTH_FAILED = 3,
    VAULT_CRYPTO_NOT_IMPLEMENTED = 4
} vault_crypto_status;

VAULT_CRYPTO_API const char *vault_crypto_status_message(vault_crypto_status status);

/* Overwrite sensitive bytes before releasing their storage. */
VAULT_CRYPTO_API void vault_crypto_secure_zero(void *buffer, size_t length);

/*
 * TODO: derive a 32-byte key from master_password and salt using Argon2id.
 * Store the KDF parameters with the encrypted vault, not in this API.
 */
VAULT_CRYPTO_API vault_crypto_status vault_crypto_derive_key(
    const uint8_t *master_password,
    size_t master_password_length,
    const uint8_t salt[VAULT_CRYPTO_SALT_BYTES],
    uint8_t key[VAULT_CRYPTO_KEY_BYTES]
);

/*
 * TODO: encrypt plaintext using XChaCha20-Poly1305.
 * ciphertext must reserve plaintext_length + VAULT_CRYPTO_TAG_BYTES bytes.
 * associated_data may be NULL only when associated_data_length is zero.
 */
VAULT_CRYPTO_API vault_crypto_status vault_crypto_encrypt(
    const uint8_t key[VAULT_CRYPTO_KEY_BYTES],
    const uint8_t nonce[VAULT_CRYPTO_NONCE_BYTES],
    const uint8_t *associated_data,
    size_t associated_data_length,
    const uint8_t *plaintext,
    size_t plaintext_length,
    uint8_t *ciphertext,
    size_t ciphertext_capacity,
    size_t *ciphertext_length
);

/* TODO: authenticate and decrypt ciphertext. Never return plaintext on auth failure. */
VAULT_CRYPTO_API vault_crypto_status vault_crypto_decrypt(
    const uint8_t key[VAULT_CRYPTO_KEY_BYTES],
    const uint8_t nonce[VAULT_CRYPTO_NONCE_BYTES],
    const uint8_t *associated_data,
    size_t associated_data_length,
    const uint8_t *ciphertext,
    size_t ciphertext_length,
    uint8_t *plaintext,
    size_t plaintext_capacity,
    size_t *plaintext_length
);

#endif
