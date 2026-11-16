#include "h_74712c1d3c73.h"

struct FUN_00c84e80_holder {
    int m_pad;
    int m_pad2;
    void* m_next;
    int __thiscall FUN_00c84e80(int* arg_2);
};

extern void __cdecl FUN_00cf0690(void* object, float value, int* data);

int FUN_00c84e80_holder::FUN_00c84e80(int* arg_2) {
    int result = 0;

    if (this != 0 && m_next != 0) {
        float value = reinterpret_cast<float*>(arg_2)[1];
        FUN_00cf0690(m_next, value, arg_2);
    } else {
        result = 1;
    }

    return result;
}