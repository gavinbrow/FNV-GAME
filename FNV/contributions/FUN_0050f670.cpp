
extern char DAT_011841cc;
extern char DAT_011846d4;
extern "C" void* __cdecl FUN_00ec43fb(void* key, int option, const void* source, const void* destination, int flags);

struct ActionObject {
    void** methods;
};

typedef void (__thiscall *ActionHandler)(ActionObject* self, int target, void* data, unsigned char mode);

struct ActionCaller {
    bool FUN_0050f670(int target, void* key, unsigned char mode, int unused, void* data);
};

bool ActionCaller::FUN_0050f670(int target, void* key, unsigned char mode, int unused, void* data)
{
    ActionObject* object = (ActionObject*)FUN_00ec43fb(key, 0, &DAT_011841cc, &DAT_011846d4, 0);
    if (object != 0 && target != 0) {
        void* savedData = data;
        ((ActionHandler)object->methods[244])(object, target, savedData, mode);
        return true;
    }
    return false;
}