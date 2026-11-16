struct Sound7390 { virtual void* __thiscall ScalarDeletingDestructor(unsigned int); int unk04; unsigned int uiFlags08; int unk0C; unsigned int uiFlags10; };
struct AudioLoadTask7390 { int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C; Sound7390* pSound; void __thiscall FUN_00ae7390(int,int); };
struct AudioHelper7390 { void __thiscall FUN_00ae6f10(); };
AudioHelper7390* __stdcall FUN_00ad9060(AudioLoadTask7390*);
void __thiscall AudioLoadTask7390::FUN_00ae7390(int,int) {
 FUN_00ad9060(this)->FUN_00ae6f10();
 unsigned int storedFlags;
 Sound7390* pDeleteFirst;
 Sound7390* pDeleteSecond2;
 if (pSound && ((storedFlags = pSound->uiFlags08) & 0x8000)) {
   pDeleteFirst = pSound;
   pDeleteSecond2 = pDeleteFirst;
   pDeleteSecond2 ? pDeleteSecond2->ScalarDeletingDestructor(1) : 0;
 } else if (pSound) {
   Sound7390 *nodeToClear = pSound;
   nodeToClear->uiFlags10 = false ? nodeToClear->uiFlags10 | 0x200u : nodeToClear->uiFlags10 & ~0x200u;
   Sound7390 *nodeToSet = pSound;
   nodeToSet->uiFlags10 = true ? nodeToSet->uiFlags10 | 0x10u : nodeToSet->uiFlags10 & ~0x10u;
 }
}
