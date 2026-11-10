#include "fragile_baby/platform.h"

#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>

int main(void)
{
    fb_platform_info_t info;
    fb_linux_info_t linux_info;

    assert(fb_platform_get_info(NULL) == FB_ERR_ARGUMENT);
    assert(fb_e2k_linux_probe(NULL) == FB_ERR_ARGUMENT);
    assert(fb_platform_get_info(&info) == FB_OK);
    assert(info.abi_version == FB_PLATFORM_ABI_VERSION);
    assert(info.struct_size == sizeof(info));
    assert(info.pointer_bits == (uint16_t)(sizeof(void *) * CHAR_BIT));
    assert(fb_e2k_generation_name(FB_E2K_GENERATION_V6)[0] == 'e');
    assert(fb_e2k_generation_name(FB_E2K_GENERATION_UNKNOWN)[0] == 'u');

#if defined(__e2k__)
    assert(info.architecture == FB_ARCH_ELBRUS_E2K);
    assert((info.flags & FB_PLATFORM_FLAG_COMPILED_FOR_E2K) != 0u);
    assert(fb_e2k_linux_probe(&linux_info) == FB_OK);
    assert(linux_info.abi_version == FB_PLATFORM_ABI_VERSION);
    assert(linux_info.machine[0] != '\0');
#else
    assert(info.architecture == FB_ARCH_HOST);
    assert((info.flags & FB_PLATFORM_FLAG_COMPILED_FOR_E2K) == 0u);
    assert(fb_e2k_linux_probe(&linux_info) == FB_ERR_UNSUPPORTED);
#endif

    (void)printf("Fragile-Baby platform tests passed. architecture=%s pointer_bits=%u\n",
        info.architecture == FB_ARCH_ELBRUS_E2K ? "e2k" : "host",
        (unsigned int)info.pointer_bits);
    return 0;
}
