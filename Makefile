CC ?= clang
CFLAGS := -std=c17 -Wall -Wextra -Wpedantic -Werror
CPPFLAGS := -Ic/include
BUILD_DIR := c/build
SOURCES := c/src/vault_crypto.c

ifeq ($(OS),Windows_NT)
LIBRARY := $(BUILD_DIR)/vaultcrypto.dll
SHARED_FLAGS := -shared
CPPFLAGS += -DVAULT_CRYPTO_BUILD
else
LIBRARY := $(BUILD_DIR)/libvaultcrypto.dylib
SHARED_FLAGS := -dynamiclib -fPIC
endif

.PHONY: all clean

all: $(LIBRARY)

$(LIBRARY): $(SOURCES) c/include/vault_crypto.h | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(CPPFLAGS) $(SHARED_FLAGS) $(SOURCES) -o $@

$(BUILD_DIR):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)
