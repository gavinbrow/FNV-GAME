#include <xmmintrin.h>
struct FUN_00dcedd0_Fields { float x, y, z, w; };
struct __declspec(align(16)) FUN_00dcedd0_Record {
    union {
        __m128 value;
        FUN_00dcedd0_Fields fields;
        unsigned char type;
    };
    void* object;
};
void __cdecl FUN_00dcedd0(const __m128* value, void* object, FUN_00dcedd0_Record** cursor)
{
    FUN_00dcedd0_Record* record = *cursor;
    record->value = *value;
    record->fields.x += 1.1920928955078125e-7;
    record->object = object;
    record->type = 0x1a;
    *cursor = record + 1;
}