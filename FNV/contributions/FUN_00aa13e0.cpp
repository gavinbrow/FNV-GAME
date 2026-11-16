struct DeviceInterface {
    virtual void Unknown();
    virtual void Dispatch(int* value, int* command, int a, int b, int c, int d, int e);
};
extern "C" DeviceInterface** DAT_011f6080;

void __cdecl FUN_00aa13e0(int value) {
    if (!value) value = 1;
    int adjusted = value;
    DeviceInterface* device = *DAT_011f6080;
    int command = 4;
    device->Dispatch(&adjusted, &command, 1, 1, 0, -1, 0);
}
