#include "h_90833f8e0811.h"

class NiObject_00a7b3d0 {
public:
    void* vtable;
    unsigned int _04;
    unsigned int _08;

    unsigned char __thiscall FUN_00a5d470(NiObject_00a7b3d0* object);
    unsigned char __thiscall FUN_00a7b3d0(NiObject_00a7b3d0* object);
};

unsigned char __thiscall NiObject_00a7b3d0::FUN_00a7b3d0(
    NiObject_00a7b3d0* object)
{
    if (!FUN_00a5d470(object))
        return 0;

    return _08 == object->_08;
}