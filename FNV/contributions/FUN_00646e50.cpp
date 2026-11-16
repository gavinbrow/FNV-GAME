struct ChanceSetting { int* __thiscall Int(); };
extern ChanceSetting DAT_011ce2fc;
extern ChanceSetting DAT_011cf2ec;
extern const double DAT_01016408;
unsigned int __cdecl FUN_00487f50();
struct ChanceModifier { int __thiscall FUN_008a16b0(); };
void __cdecl FUN_00646e50(void* unused, ChanceModifier* modifier, int baseChance, int effectChance, int extraChance, bool fixedChance, unsigned char* success, unsigned char* critical)
{
    *success = 0;
    *critical = 0;
    unsigned int normalChance = FUN_00487f50() % 100;
    int intermediateChance;
    if (fixedChance) {
        intermediateChance = baseChance + extraChance;
    } else {
        int criticalBase = extraChance + *DAT_011ce2fc.Int();
        intermediateChance = (int)((double)criticalBase * ((double)baseChance * DAT_01016408));
    }
    int criticalChance = intermediateChance;
    int roll = effectChance + *DAT_011cf2ec.Int();
    if ((int)normalChance < criticalChance) {
        *critical = 1;
    } else if ((int)normalChance < roll) {
        *success = 1;
    }
    if (modifier && (*critical || *success)) {
        switch (modifier->FUN_008a16b0()) {
        case 1:
            *critical = 0;
            *success = 1;
            break;
        case 2:
            *critical = 1;
            *success = 0;
            break;
        case 3:
            *critical = 0;
            *success = 0;
            break;
        }
    }
}