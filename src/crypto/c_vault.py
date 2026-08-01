"""Minimal ctypes contract for the platform-specific vaultcrypto library."""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_LIBRARY_NAME = "vaultcrypto.dll" if sys.platform == "win32" else "libvaultcrypto.dylib"
_DEFAULT_LIBRARY = _ROOT / "c" / "build" / _LIBRARY_NAME

STATUS_OK = 0
STATUS_NOT_IMPLEMENTED = 4
SALT_BYTES = 16
KEY_BYTES = 32

class VaultCryptoError(RuntimeError):
    """Raised when the C library rejects a cryptographic operation."""

class VaultCrypto:
    def __init__(self, library_path: Path = _DEFAULT_LIBRARY) -> None:
        self._library = ctypes.CDLL(str(library_path))
        self._configure_signatures()

    def _configure_signatures(self) -> None:
        self._library.vault_crypto_derive_key.argtypes = (
            ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8),
        )
        self._library.vault_crypto_derive_key.restype = ctypes.c_int
        self._library.vault_crypto_status_message.argtypes = (ctypes.c_int,)
        self._library.vault_crypto_status_message.restype = ctypes.c_char_p

    def derive_key(self, master_password: bytes, salt: bytes) -> bytes:
        if len(salt) != SALT_BYTES:
            raise ValueError(f"salt must contain exactly {SALT_BYTES} bytes")
        if not master_password:
            raise ValueError("master_password cannot be empty")

        password_buffer = (ctypes.c_uint8 * len(master_password)).from_buffer_copy(master_password)
        salt_buffer = (ctypes.c_uint8 * SALT_BYTES).from_buffer_copy(salt)
        key_buffer = (ctypes.c_uint8 * KEY_BYTES)()
        status = self._library.vault_crypto_derive_key(
            password_buffer, len(master_password), salt_buffer, key_buffer
        )
        if status != STATUS_OK:
            message = self._library.vault_crypto_status_message(status).decode("utf-8")
            raise VaultCryptoError(message)
        return bytes(key_buffer)
