
struct FUN_004a4650_ListBase;
void __fastcall FUN_004a4650(FUN_004a4650_ListBase* self);
struct ObstacleBase { ~ObstacleBase(); };
struct FUN_004a44a0 : ObstacleBase {
   ~FUN_004a44a0();
};
FUN_004a44a0::~FUN_004a44a0() {
    FUN_004a4650(reinterpret_cast<FUN_004a4650_ListBase*>(this));
}
