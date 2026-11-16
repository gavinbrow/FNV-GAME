extern float DAT_01012054;
extern double DAT_01012060;
struct BookForm { unsigned int FUN_00401170(); float FUN_004be060(); };
unsigned int __cdecl FUN_004873d0(BookForm*);
float __cdecl FUN_00646360(unsigned short, float);
void __cdecl FUN_00476b20(float);
struct ItemChangeCalc { int unknown00; int unknown04; BookForm* item; float FUN_004bcdb0(int); void FUN_004bdf90(int unused); };
void ItemChangeCalc::FUN_004bdf90(int unused) {
 float result = DAT_01012054;
 if (item->FUN_00401170() == 0x18) {
 BookForm* current = item;
 float count = (float)FUN_004873d0(current);
 float multiplier = (float)(count == DAT_01012060 ? 0.0 : FUN_004bcdb0(0) / count);
 result = FUN_00646360((unsigned short)current->FUN_004be060(), multiplier);
 }
 FUN_00476b20(result);
}