extern "C" char str_01070244[];
int __cdecl FUN_00a00940(const char*, int);

struct SelectedObject {
    bool __thiscall FUN_00a01230(int);
};

struct FUN_00721440_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    SelectedObject* selected;

    bool __thiscall FUN_00724430();
    bool __thiscall FUN_007242f0(SelectedObject* object);
    void __thiscall FUN_007244e0();
    bool __thiscall FUN_00721440(SelectedObject* object);
};

bool FUN_00721440_class::FUN_00721440(SelectedObject* object)
{
    if (FUN_00724430() &&
        (!object || (FUN_007242f0(object) &&
            object->FUN_00a01230(FUN_00a00940(str_01070244, -1))))) {
        selected = object;
        FUN_007244e0();
        return true;
    } else {
        return false;
    }
}
