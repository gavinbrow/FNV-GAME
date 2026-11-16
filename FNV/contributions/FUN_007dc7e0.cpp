
extern const char UNK_01074eb8;
extern const char UNK_0106f8f8;
extern const char UNK_010702d8;
extern const char UNK_01070250;
extern double DAT_01012070;

int __cdecl FUN_00a01860(const char* name);
int __cdecl FUN_0066e9f0(void* value);
int __cdecl FUN_0066e9b0(void* value);
unsigned int __cdecl FUN_0066ea20(void* value);
float __cdecl FUN_00404010(float low, float high);
float __cdecl FUN_004e4430(float value);

struct ChildList007dc7e0 {
    Tile** FUN_0073ac90();
    Tile** FUN_007b5370();
};
struct TileAdapter007dc7e0 {
    void FUN_00700320(int trait, int value);
    void FUN_00a01350(int trait, int value, bool update);
    float FUN_00a011b0(int trait);
    TileAdapter007dc7e0* FUN_0045cd60();
    void FUN_00a04640(int value);
    void FUN_00a012d0(int trait, float value, bool update);
    void FUN_00a01290(int trait, float value);
};
struct StatsMenuFunction007dc7e0 : StatsMenu {
    void FUN_007dc7e0(void* actor);
};
void StatsMenuFunction007dc7e0::FUN_007dc7e0(void* actor) {
    TileAdapter007dc7e0* pMain = *(reinterpret_cast<TileAdapter007dc7e0**>(reinterpret_cast<ChildList007dc7e0*>((char*)pTiles[26]+4)->FUN_0073ac90()));
    TileAdapter007dc7e0* second = *(reinterpret_cast<TileAdapter007dc7e0**>(reinterpret_cast<ChildList007dc7e0*>((char*)pTiles[26]+4)->FUN_007b5370()));
    float maxValue = second->FUN_00a011b0(FUN_00a01860(&UNK_01074eb8));
    float diff = 0.0f;
    reinterpret_cast<TileAdapter007dc7e0*>(pTiles[25])->FUN_00700320(0xfa3,1);
    reinterpret_cast<TileAdapter007dc7e0*>(pTiles[25])->FUN_00a01350(0xfcc,FUN_0066e9f0(actor),true);
    pMain->FUN_00a01350(0xfc4,FUN_0066e9b0(actor),true);
    unsigned int amount = FUN_0066ea20(actor);
    if (amount > 0) {
        reinterpret_cast<TileAdapter007dc7e0*>(pTiles[52])->FUN_00700320(0xfa3,1);
        reinterpret_cast<TileAdapter007dc7e0*>(pTiles[52])->FUN_00a01350(0xfcc,amount,true);
    } else {
        reinterpret_cast<TileAdapter007dc7e0*>(pTiles[52])->FUN_00700320(0xfa3,0);
    }
    pMain->FUN_00a04640(0);
    diff = pMain->FUN_00a011b0(0xfb0) - pMain->FUN_0045cd60()->FUN_00a011b0(0xfb0);
    diff = FUN_00404010(0.0f,diff);
    second->FUN_00a012d0(FUN_00a01860(&UNK_0106f8f8), FUN_004e4430(diff / maxValue) + DAT_01012070, true);
    second->FUN_00a012d0(FUN_00a01860(&UNK_010702d8), 0.0f, false);
    second->FUN_00a01290(FUN_00a01860(&UNK_01070250), 1.0f);
}
