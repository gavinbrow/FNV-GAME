struct MenuDisplay { void FUN_00a01350(unsigned, const char*, int); void FUN_00700320(unsigned, int); };
struct MessageTemplate { const char* FUN_00403df0(); };
extern MessageTemplate DAT_011d4558, DAT_011d2c10;
int _sprintf_s(char*, unsigned, const char*, ...);
struct TraitMenu_007e71b0 { void* unk00; void* unk04; void* unk08; void* unk0c; void* unk10; void* unk14; void* unk18; void* unk1c;
void* unk20; void* unk24; void* unk28; void* unk2c; void* unk30; void* unk34;
MenuDisplay* tile38; void* unk3c; void* unk40; void* unk44; void* unk48;
int firstValue; int lastValue; void FUN_007e71b0(); };
void TraitMenu_007e71b0::FUN_007e71b0() { char message[64]; { int difference = lastValue - firstValue; if (difference == 1) {
_sprintf_s(message,64,DAT_011d4558.FUN_00403df0(),difference);
tile38->FUN_00a01350(0xfc4,message,1);
tile38->FUN_00700320(0xfa3,1);
} else {
_sprintf_s(message,64,DAT_011d2c10.FUN_00403df0(),difference);
tile38->FUN_00a01350(0xfc4,message,1);
tile38->FUN_00700320(0xfa3,1);
} } }