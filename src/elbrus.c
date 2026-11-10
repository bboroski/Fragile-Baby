#include "fragile_baby/elbrus.h"

#include <stddef.h>

static int has_text(const char *value)
{
    return value != NULL && value[0] != '\0';
}

static int evidence_valid(fb_evidence_state_t state, const char *reference)
{
    if (state == FB_EVIDENCE_UNKNOWN) {
        return !has_text(reference);
    }
    if (state == FB_EVIDENCE_PASS || state == FB_EVIDENCE_FAIL) {
        return has_text(reference);
    }
    return 0;
}

fb_elbrus_status_t fb_elbrus_evaluate(
    const fb_elbrus_profile_t *profile,
    fb_elbrus_stage_t *stage_out)
{
    if (profile == NULL || stage_out == NULL) {
        return FB_ELBRUS_EINVAL;
    }
    if (profile->profile_version != FB_ELBRUS_PROFILE_VERSION) {
        return FB_ELBRUS_EVERSION;
    }
    if (!evidence_valid(profile->toolchain_probe, profile->toolchain_evidence) ||
        !evidence_valid(profile->abi_probe, profile->abi_evidence) ||
        !evidence_valid(profile->hardware_bringup, profile->hardware_evidence)) {
        return FB_ELBRUS_EEVIDENCE;
    }

    if (!has_text(profile->profile_id) ||
        !has_text(profile->cpu_model) ||
        !has_text(profile->compiler_path) ||
        !has_text(profile->compiler_version) ||
        !has_text(profile->sysroot) ||
        !has_text(profile->abi_name) ||
        (profile->pointer_bits != 32U && profile->pointer_bits != 64U &&
         profile->pointer_bits != 128U) ||
        (profile->endianness != FB_ENDIAN_LITTLE &&
         profile->endianness != FB_ENDIAN_BIG)) {
        *stage_out = FB_ELBRUS_NEEDS_CONFIGURATION;
        return FB_ELBRUS_OK;
    }

    if (profile->toolchain_probe == FB_EVIDENCE_FAIL) {
        *stage_out = FB_ELBRUS_TOOLCHAIN_BLOCKED;
    } else if (profile->toolchain_probe == FB_EVIDENCE_UNKNOWN) {
        *stage_out = FB_ELBRUS_TOOLCHAIN_PENDING;
    } else if (profile->abi_probe == FB_EVIDENCE_FAIL) {
        *stage_out = FB_ELBRUS_ABI_BLOCKED;
    } else if (profile->abi_probe == FB_EVIDENCE_UNKNOWN) {
        *stage_out = FB_ELBRUS_ABI_PENDING;
    } else if (profile->hardware_bringup == FB_EVIDENCE_FAIL) {
        *stage_out = FB_ELBRUS_HARDWARE_BLOCKED;
    } else if (profile->hardware_bringup == FB_EVIDENCE_UNKNOWN) {
        *stage_out = FB_ELBRUS_HARDWARE_PENDING;
    } else {
        *stage_out = FB_ELBRUS_QUALIFIED;
    }
    return FB_ELBRUS_OK;
}

const char *fb_elbrus_stage_name(fb_elbrus_stage_t stage)
{
    switch (stage) {
        case FB_ELBRUS_NEEDS_CONFIGURATION: return "needs_configuration";
        case FB_ELBRUS_TOOLCHAIN_PENDING: return "toolchain_pending";
        case FB_ELBRUS_TOOLCHAIN_BLOCKED: return "toolchain_blocked";
        case FB_ELBRUS_ABI_PENDING: return "abi_pending";
        case FB_ELBRUS_ABI_BLOCKED: return "abi_blocked";
        case FB_ELBRUS_HARDWARE_PENDING: return "hardware_pending";
        case FB_ELBRUS_HARDWARE_BLOCKED: return "hardware_blocked";
        case FB_ELBRUS_QUALIFIED: return "qualified";
        default: return "invalid";
    }
}
