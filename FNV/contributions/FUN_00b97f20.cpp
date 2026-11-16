struct Dispatcher {
    void** vtable;
    __forceinline void Notify(int eventType, int argument, int unused1, int unused2) {
        typedef void (__thiscall *Notification)(Dispatcher*, int, int, int, int);
        Notification call = reinterpret_cast<Notification>(vtable[26]);
        call(this, eventType, argument, unused1, unused2);
    }
};

__forceinline Dispatcher* GetDispatcher(NiRenderer* renderer) {
    return *reinterpret_cast<Dispatcher**>(reinterpret_cast<char*>(renderer) + 0x8b8);
}

extern NiRenderer* DAT_011f9508;
extern int DAT_011ff9d8[];
extern int DAT_011ffa94;
extern int DAT_011ffa90;
extern int DAT_011ad888[];

void __cdecl FUN_00b97f20(int index, int secondValue, int increment) {
    int firstChannel = DAT_011ffa94;
    if (DAT_011ff9d8[firstChannel] == 0) {
        GetDispatcher(DAT_011f9508)->Notify(0x19, DAT_011ad888[index], 0, 0);
    }
    DAT_011ff9d8[firstChannel] += increment;
    int secondChannel = DAT_011ffa90;
    if (DAT_011ff9d8[secondChannel] == 0) {
        GetDispatcher(DAT_011f9508)->Notify(0x18, secondValue, 0, 0);
    }
    DAT_011ff9d8[secondChannel] += increment;
}
