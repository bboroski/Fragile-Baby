#include "fragile_baby/platform.h"

#if defined(__linux__)
#include <stdio.h>
#include <string.h>
#include <sys/utsname.h>
#include <unistd.h>

static void fb_copy_text(char *destination, size_t capacity, const char *source)
{
    size_t index = 0u;

    if (destination == NULL || capacity == 0u || source == NULL) {
        return;
    }
    while ((index + 1u) < capacity && source[index] != '\0') {
        destination[index] = source[index];
        index++;
    }
    destination[index] = '\0';
}

static void fb_trim(char *text)
{
    size_t length;

    if (text == NULL) {
        return;
    }
    while (*text == ' ' || *text == '\t') {
        const size_t remaining = strlen(text);
        memmove(text, text + 1, remaining);
    }
    length = strlen(text);
    while (length > 0u &&
           (text[length - 1u] == '\n' || text[length - 1u] == '\r' ||
            text[length - 1u] == ' ' || text[length - 1u] == '\t')) {
        text[length - 1u] = '\0';
        length--;
    }
}

static void fb_read_cpu_model(char *output, size_t capacity)
{
    FILE *file = fopen("/proc/cpuinfo", "r");
    char line[256];

    if (file == NULL || output == NULL || capacity == 0u) {
        if (file != NULL) {
            (void)fclose(file);
        }
        return;
    }

    while (fgets(line, (int)sizeof(line), file) != NULL) {
        const char *separator = strchr(line, ':');
        if (separator == NULL) {
            continue;
        }
        if (strncmp(line, "model name", 10u) == 0 ||
            strncmp(line, "cpu model", 9u) == 0 ||
            strncmp(line, "CPU", 3u) == 0) {
            fb_copy_text(output, capacity, separator + 1);
            fb_trim(output);
            if (output[0] != '\0') {
                break;
            }
        }
    }

    (void)fclose(file);
}
#endif

fb_status_t fb_e2k_linux_probe(fb_linux_info_t *out_info)
{
    if (out_info == NULL) {
        return FB_ERR_ARGUMENT;
    }

#if defined(__linux__) && defined(__e2k__)
    {
        struct utsname system_info;
        const long processors = sysconf(_SC_NPROCESSORS_ONLN);

        memset(out_info, 0, sizeof(*out_info));
        if (uname(&system_info) != 0) {
            return FB_ERR_IO;
        }

        out_info->abi_version = FB_PLATFORM_ABI_VERSION;
        out_info->struct_size = (uint32_t)sizeof(*out_info);
        out_info->online_processors = (processors > 0L) ? (uint32_t)processors : 0u;
        fb_copy_text(out_info->machine, sizeof(out_info->machine), system_info.machine);
        fb_copy_text(out_info->kernel_release, sizeof(out_info->kernel_release),
                     system_info.release);
        fb_read_cpu_model(out_info->cpu_model, sizeof(out_info->cpu_model));
        return FB_OK;
    }
#else
    (void)out_info;
    return FB_ERR_UNSUPPORTED;
#endif
}
