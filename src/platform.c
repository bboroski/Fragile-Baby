#include "fragile_baby/platform.h"

#include <limits.h>
#include <stddef.h>
#include <string.h>

static int fb_is_little_endian(void)
{
    const uint32_t value = UINT32_C(1);
    return ((const unsigned char *)&value)[0] == 1u;
}

fb_status_t fb_platform_get_info(fb_platform_info_t *out_info)
{
    if (out_info == NULL) {
        return FB_ERR_ARGUMENT;
    }

    memset(out_info, 0, sizeof(*out_info));
    out_info->abi_version = FB_PLATFORM_ABI_VERSION;
    out_info->struct_size = (uint32_t)sizeof(*out_info);
    out_info->pointer_bits = (uint16_t)(sizeof(void *) * CHAR_BIT);
    out_info->architecture = FB_ARCH_HOST;

#if defined(__e2k__)
    out_info->architecture = FB_ARCH_ELBRUS_E2K;
    out_info->flags |= FB_PLATFORM_FLAG_COMPILED_FOR_E2K;
#endif

#if defined(__LCC__)
    out_info->compiler_family = FB_COMPILER_LCC;
    out_info->compiler_major = (uint32_t)__LCC__;
#elif defined(__clang__)
    out_info->compiler_family = FB_COMPILER_CLANG;
    out_info->compiler_major = (uint32_t)__clang_major__;
#elif defined(__GNUC__)
    out_info->compiler_family = FB_COMPILER_GCC_COMPATIBLE;
    out_info->compiler_major = (uint32_t)__GNUC__;
#else
    out_info->compiler_family = FB_COMPILER_UNKNOWN;
#endif

#if defined(FB_E2K_GENERATION) && (FB_E2K_GENERATION >= 1) && (FB_E2K_GENERATION <= 7)
    out_info->generation = (uint16_t)FB_E2K_GENERATION;
#else
    out_info->generation = (uint16_t)FB_E2K_GENERATION_UNKNOWN;
#endif

    if (fb_is_little_endian()) {
        out_info->flags |= FB_PLATFORM_FLAG_LITTLE_ENDIAN;
    }
    if (out_info->pointer_bits == 128u) {
        out_info->flags |= FB_PLATFORM_FLAG_POINTERS_128_BIT;
    }

    return FB_OK;
}

const char *fb_e2k_generation_name(fb_e2k_generation_t generation)
{
    switch (generation) {
    case FB_E2K_GENERATION_V1: return "e2k-v1";
    case FB_E2K_GENERATION_V2: return "e2k-v2";
    case FB_E2K_GENERATION_V3: return "e2k-v3";
    case FB_E2K_GENERATION_V4: return "e2k-v4";
    case FB_E2K_GENERATION_V5: return "e2k-v5";
    case FB_E2K_GENERATION_V6: return "e2k-v6";
    case FB_E2K_GENERATION_V7: return "e2k-v7";
    case FB_E2K_GENERATION_UNKNOWN:
    default: return "unknown";
    }
}
