#ifndef FRAGILE_BABY_PLATFORM_H
#define FRAGILE_BABY_PLATFORM_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define FB_PLATFORM_ABI_VERSION UINT32_C(1)
#define FB_PLATFORM_TEXT_CAPACITY 96u

typedef int32_t fb_status_t;

enum {
    FB_OK = 0,
    FB_ERR_ARGUMENT = -1,
    FB_ERR_UNSUPPORTED = -2,
    FB_ERR_IO = -3
};

typedef enum fb_architecture {
    FB_ARCH_HOST = 0,
    FB_ARCH_ELBRUS_E2K = 1
} fb_architecture_t;

typedef enum fb_e2k_generation {
    FB_E2K_GENERATION_UNKNOWN = 0,
    FB_E2K_GENERATION_V1 = 1,
    FB_E2K_GENERATION_V2 = 2,
    FB_E2K_GENERATION_V3 = 3,
    FB_E2K_GENERATION_V4 = 4,
    FB_E2K_GENERATION_V5 = 5,
    FB_E2K_GENERATION_V6 = 6,
    FB_E2K_GENERATION_V7 = 7
} fb_e2k_generation_t;

typedef enum fb_compiler_family {
    FB_COMPILER_UNKNOWN = 0,
    FB_COMPILER_LCC = 1,
    FB_COMPILER_CLANG = 2,
    FB_COMPILER_GCC_COMPATIBLE = 3
} fb_compiler_family_t;

enum {
    FB_PLATFORM_FLAG_COMPILED_FOR_E2K = UINT32_C(1) << 0,
    FB_PLATFORM_FLAG_LITTLE_ENDIAN = UINT32_C(1) << 1,
    FB_PLATFORM_FLAG_POINTERS_128_BIT = UINT32_C(1) << 2
};

typedef struct fb_platform_info {
    uint32_t abi_version;
    uint32_t struct_size;
    uint32_t flags;
    uint32_t compiler_major;
    uint16_t pointer_bits;
    uint16_t generation;
    uint16_t compiler_family;
    uint16_t reserved;
    fb_architecture_t architecture;
} fb_platform_info_t;

typedef struct fb_linux_info {
    uint32_t abi_version;
    uint32_t struct_size;
    uint32_t online_processors;
    char machine[32];
    char kernel_release[64];
    char cpu_model[FB_PLATFORM_TEXT_CAPACITY];
} fb_linux_info_t;

/* Compile-target facts only; this function does not probe privileged hardware. */
fb_status_t fb_platform_get_info(fb_platform_info_t *out_info);

/* Linux userspace metadata probe. Returns FB_ERR_UNSUPPORTED on non-E2K builds. */
fb_status_t fb_e2k_linux_probe(fb_linux_info_t *out_info);

const char *fb_e2k_generation_name(fb_e2k_generation_t generation);

#ifdef __cplusplus
}
#endif

#endif
