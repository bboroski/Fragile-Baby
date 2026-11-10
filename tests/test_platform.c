#include "fragile_baby/platform.h"

#include <limits.h>
#include <stdio.h>

#define CHECK(condition)                                                        \
    do {                                                                        \
        if (!(condition)) {                                                     \
            (void)fprintf(stderr, "CHECK failed: %s (%s:%d)\n",                \
                          #condition, __FILE__, __LINE__);                      \
            return 1;                                                           \
        }                                                                       \
    } while (0)

int main(void)
{
    fb_platform_info_t info;

    CHECK(fb_platform_get_info(NULL) == FB_ERR_ARGUMENT);
    CHECK(fb_e2k_linux_probe(NULL) == FB_ERR_ARGUMENT);
    CHECK(fb_platform_get_info(&info) == FB_OK);
    CHECK(info.abi_version == FB_PLATFORM_ABI_VERSION);
    CHECK(info.struct_size == sizeof(info));
    CHECK(info.pointer_bits == (uint16_t)(sizeof(void *) * CHAR_BIT));
    CHECK(fb_e2k_generation_name(FB_E2K_GENERATION_V6)[0] == 'e');
    CHECK(fb_e2k_generation_name(FB_E2K_GENERATION_UNKNOWN)[0] == 'u');

#if defined(__e2k__)
    {
        fb_linux_info_t linux_info;
        CHECK(info.architecture == FB_ARCH_ELBRUS_E2K);
        CHECK((info.flags & FB_PLATFORM_FLAG_COMPILED_FOR_E2K) != 0u);
        CHECK(fb_e2k_linux_probe(&linux_info) == FB_OK);
        CHECK(linux_info.abi_version == FB_PLATFORM_ABI_VERSION);
        CHECK(linux_info.machine[0] != '\0');
    }
#else
    CHECK(info.architecture == FB_ARCH_HOST);
    CHECK((info.flags & FB_PLATFORM_FLAG_COMPILED_FOR_E2K) == 0u);
    {
        fb_linux_info_t linux_info;
        CHECK(fb_e2k_linux_probe(&linux_info) == FB_ERR_UNSUPPORTED);
    }
#endif

    (void)printf("Fragile-Baby platform tests passed. architecture=%s pointer_bits=%u\n",
                 info.architecture == FB_ARCH_ELBRUS_E2K ? "e2k" : "host",
                 (unsigned int)info.pointer_bits);
    return 0;
}
