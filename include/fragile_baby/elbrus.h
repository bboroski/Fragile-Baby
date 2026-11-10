#ifndef FRAGILE_BABY_ELBRUS_H
#define FRAGILE_BABY_ELBRUS_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define FB_ELBRUS_PROFILE_VERSION 1U

typedef enum {
    FB_EVIDENCE_UNKNOWN = 0,
    FB_EVIDENCE_PASS = 1,
    FB_EVIDENCE_FAIL = 2
} fb_evidence_state_t;

typedef enum {
    FB_ENDIAN_UNKNOWN = 0,
    FB_ENDIAN_LITTLE = 1,
    FB_ENDIAN_BIG = 2
} fb_endianness_t;

typedef enum {
    FB_ELBRUS_NEEDS_CONFIGURATION = 0,
    FB_ELBRUS_TOOLCHAIN_PENDING,
    FB_ELBRUS_TOOLCHAIN_BLOCKED,
    FB_ELBRUS_ABI_PENDING,
    FB_ELBRUS_ABI_BLOCKED,
    FB_ELBRUS_HARDWARE_PENDING,
    FB_ELBRUS_HARDWARE_BLOCKED,
    FB_ELBRUS_QUALIFIED
} fb_elbrus_stage_t;

typedef enum {
    FB_ELBRUS_OK = 0,
    FB_ELBRUS_EINVAL = -1,
    FB_ELBRUS_EVERSION = -2,
    FB_ELBRUS_EEVIDENCE = -3
} fb_elbrus_status_t;

typedef struct {
    uint32_t profile_version;
    const char *profile_id;
    const char *cpu_model;
    const char *compiler_path;
    const char *compiler_version;
    const char *sysroot;
    const char *abi_name;
    uint32_t pointer_bits;
    fb_endianness_t endianness;

    fb_evidence_state_t toolchain_probe;
    const char *toolchain_evidence;
    fb_evidence_state_t abi_probe;
    const char *abi_evidence;
    fb_evidence_state_t hardware_bringup;
    const char *hardware_evidence;
} fb_elbrus_profile_t;

/*
 * Evaluate the next qualification gate. Missing configuration is a state,
 * not an implicit default. PASS/FAIL evidence must point to a retained report.
 */
fb_elbrus_status_t fb_elbrus_evaluate(
    const fb_elbrus_profile_t *profile,
    fb_elbrus_stage_t *stage_out);

const char *fb_elbrus_stage_name(fb_elbrus_stage_t stage);

#ifdef __cplusplus
}
#endif

#endif
