#include <string.h>
void __cdecl FUN_00aa2a00(char *);
void __cdecl FUN_00aa2a70(char *);
char __cdecl FUN_00aa2cc0(char *);
char * __cdecl FUN_00aa2c50(char *);

void __cdecl FUN_00aa2ac0(char *path)
{
    FUN_00aa2a00(path);
    FUN_00aa2a70(path);
    if (FUN_00aa2cc0(path)) {
        if (!path) return;
        while (*path == '.' || *path == '\\') {
            ++path;
            if (!path) return;
        }
    } else {
        path = FUN_00aa2c50(path);
    }
    if (!path) return;
    char *end = path + strlen(path) + 1;
    unsigned int pattern = 0x002e2e5c;
    char *found = strstr(path, (char *)&pattern);
    while (found) {
        *found = 0;
        char *dst = strrchr(path, '\\');
        if (dst) {
            found += 3;
        } else {
            if (found + 3)
                found += 4;
            else
                found = 0;
            dst = path;
        }
        int remaining = (int)end - (int)found;
        if (remaining > 0) {
            int shift = (int)found - (int)dst;
            do {
                *dst = dst[shift];
                ++dst;
                --remaining;
            } while (remaining);
        }
        found = strstr(path, (char*)&pattern);
    }
}