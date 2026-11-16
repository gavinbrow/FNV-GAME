struct Item {
    bool __thiscall FUN_00a01230(int);
};
extern int UNK_01070244;
int __cdecl FUN_00a00940(int*,int);

struct Object {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    Item* current;
    bool __thiscall FUN_0072bc30();
    bool __thiscall FUN_007242f0(Item*);
    void __thiscall FUN_0072bce0();
    bool __thiscall FUN_0072a250(Item* input);
};

bool __thiscall Object::FUN_0072a250(Item* input) {
    if (FUN_0072bc30() && (!input || (FUN_007242f0(input) && input->FUN_00a01230(FUN_00a00940(&UNK_01070244,-1))))) {
      current = input;
      FUN_0072bce0();
      return true;
    } else {
      return false;
    }
}