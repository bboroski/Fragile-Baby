#include "fragile_baby/elbrus.h"

#include <assert.h>
#include <stdio.h>

int main(void)
{
    fb_elbrus_profile_t profile = {0};
    fb_elbrus_stage_t stage = FB_ELBRUS_NEEDS_CONFIGURATION;

    profile.profile_version = FB_ELBRUS_PROFILE_VERSION;
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_NEEDS_CONFIGURATION);

    profile.profile_id = "e2k-target";
    profile.cpu_model = "operator-specified";
    profile.compiler_path = "/opt/toolchain/bin/compiler";
    profile.compiler_version = "operator-specified";
    profile.sysroot = "/opt/sysroot";
    profile.abi_name = "operator-specified";
    profile.pointer_bits = 64U;
    profile.endianness = FB_ENDIAN_LITTLE;

    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_TOOLCHAIN_PENDING);

    profile.toolchain_probe = FB_EVIDENCE_PASS;
    profile.toolchain_evidence = "reports/toolchain-smoke-test.txt";
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_ABI_PENDING);

    profile.abi_probe = FB_EVIDENCE_PASS;
    profile.abi_evidence = "reports/abi-layout-probe.txt";
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_HARDWARE_PENDING);

    profile.hardware_bringup = FB_EVIDENCE_PASS;
    profile.hardware_evidence = "reports/target-bringup.txt";
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_QUALIFIED);
    assert(fb_elbrus_stage_name(stage)[0] == 'q');

    profile.hardware_bringup = FB_EVIDENCE_FAIL;
    profile.hardware_evidence = "reports/failed-target-bringup.txt";
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_OK);
    assert(stage == FB_ELBRUS_HARDWARE_BLOCKED);

    profile.hardware_bringup = FB_EVIDENCE_PASS;
    profile.hardware_evidence = NULL;
    assert(fb_elbrus_evaluate(&profile, &stage) == FB_ELBRUS_EEVIDENCE);

    puts("Fragile-Baby Elbrus qualification tests: PASS");
    return 0;
}
