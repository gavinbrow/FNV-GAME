extern int DAT_011ad8a8[];
extern void* DAT_011f9508;
extern int DAT_011ff9d8[];
extern unsigned int DAT_011ffb04;
extern unsigned int DAT_011ffb08;
extern unsigned int DAT_011ffb0c;
struct DeviceView { void** vtable; };
void __cdecl FUN_00b980c0(int first, int second, int third, int delta) {
    if (DAT_011ff9d8[DAT_011ffb04] == 0) {
        void* renderer = *(void* volatile*)&DAT_011f9508;
        DeviceView* device = *(DeviceView**)((char*)renderer + 0x8b8);
        ((void (__thiscall *)(DeviceView*, unsigned int, int, int, int))device->vtable[26])(device, 0x35, DAT_011ad8a8[first + 11], 0, 0);
    }
    if (DAT_011ff9d8[DAT_011ffb08] == 0) {
        void* renderer = *(void* volatile*)&DAT_011f9508;
        DeviceView* device = *(DeviceView**)((char*)renderer + 0x8b8);
        ((void (__thiscall *)(DeviceView*, unsigned int, int, int, int))device->vtable[26])(device, 0x36, DAT_011ad8a8[second + 11], 0, 0);
    }
    unsigned int index = DAT_011ffb0c;
    if (DAT_011ff9d8[index] == 0) {
        void* renderer = DAT_011f9508;
        DeviceView* device = *(DeviceView**)((char*)renderer + 0x8b8);
        ((void (__thiscall *)(DeviceView*, unsigned int, int, int, int))device->vtable[26])(device, 0x37, DAT_011ad8a8[third + 11], 0, 0);
    }
    DAT_011ff9d8[index] += delta;
}


