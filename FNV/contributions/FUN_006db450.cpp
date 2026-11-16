struct FUN_006db450_Element {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    void __thiscall FUN_006cf900(void* argument);
};
struct FUN_006db450_Owner {
    unsigned int unk00;
    FUN_006db450_Element* elements;
    int __thiscall FUN_006dc260();
    void __thiscall FUN_006d05e0(FUN_006db450_Element* element, bool enabled);
    int __thiscall FUN_006db450(void* argument);
};
int __thiscall FUN_006db450_Owner::FUN_006db450(void* argument) {
    int index = FUN_006dc260();
    FUN_006d05e0(&elements[index], true);
    elements[index].FUN_006cf900(argument);
    return index;
}