typedef int (__thiscall *FUN_00d42a60_method)(void*);
struct FUN_00d42a60_vtable {
    FUN_00d42a60_method slot00;
    FUN_00d42a60_method slot04;
    FUN_00d42a60_method slot08;
    FUN_00d42a60_method slot0c;
    FUN_00d42a60_method slot10;
    FUN_00d42a60_method slot14;
    FUN_00d42a60_method slot18;
    FUN_00d42a60_method slot1c;
    FUN_00d42a60_method slot20;
    FUN_00d42a60_method slot24;
    FUN_00d42a60_method slot28;
    FUN_00d42a60_method slot2c;
    FUN_00d42a60_method slot30;
    FUN_00d42a60_method slot34;
};
struct FUN_00d42a60_interface {
    FUN_00d42a60_vtable* vtable;
};
struct FUN_00d42a60_class {
    void* unk00;
    void* unk04;
    void* unk08;
    FUN_00d42a60_interface* unk0c;
    int __thiscall FUN_00d42a60();
};
int FUN_00d42a60_class::FUN_00d42a60() {
    FUN_00d42a60_method method = unk0c->vtable->slot34;
    return method(unk0c);
}

