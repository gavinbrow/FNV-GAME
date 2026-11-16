extern "C" int __fastcall FUN_004503f0(void*);
extern "C" unsigned char __fastcall FUN_00450ff0(void*);

struct TESBuffer45130 : Zt5TES {
    void FUN_00455130(TESObjectCELL* apCell);
};

void TESBuffer45130::FUN_00455130(TESObjectCELL* apCell)
{
    if (apCell == 0)
        return;

    int index = 0;
    int last = FUN_004503f0(&DAT_011c3c90) - 1;
    for (; index < last; ++index) {
        if (apCell == ((TESObjectCELL**)pExteriorBuffer)[index]) {
            TESObjectCELL* nextCell;
            for (; index < last; ++index) {
                nextCell = ((TESObjectCELL**)pExteriorBuffer)[index + 1];
                if (!(nextCell != 0 && FUN_00450ff0(nextCell)))
                    break;
                ((TESObjectCELL**)pExteriorBuffer)[index] = nextCell;
            }
            ((TESObjectCELL**)pExteriorBuffer)[index] = apCell;
            return;
        } else {
            if (((TESObjectCELL**)pExteriorBuffer)[index] == 0)
                return;
        }
    }
}