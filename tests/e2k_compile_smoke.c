#include "fragile_baby/platform.h"

#ifndef __e2k__
#error "This target must be compiled by an Elbrus e2k compiler"
#endif

int main(void)
{
    fb_platform_info_t info;

    if (fb_platform_get_info(&info) != FB_OK) {
        return 1;
    }
    if (info.architecture != FB_ARCH_ELBRUS_E2K) {
        return 2;
    }
    if ((info.flags & FB_PLATFORM_FLAG_COMPILED_FOR_E2K) == 0u) {
        return 3;
    }
    return 0;
}
