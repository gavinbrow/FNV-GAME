
struct S004eee_Controller {
 virtual void slot_00();
 virtual void slot_04();
 virtual void slot_08();
 virtual void slot_0c();
 virtual void slot_10();
 virtual void slot_14();
 virtual void slot_18();
 virtual void slot_1c();
 virtual void slot_20();
 virtual void slot_24();
 virtual void slot_28();
 virtual void slot_2c();
 virtual void slot_30();
 virtual void slot_34();
 virtual void slot_38();
 virtual void slot_3c();
 virtual void slot_40();
 virtual void slot_44();
 virtual void slot_48();
 virtual void slot_4c();
 virtual void slot_50();
 virtual void slot_54();
 virtual void slot_58();
 virtual void slot_5c();
 virtual void slot_60();
 virtual void slot_64();
 virtual void slot_68();
 virtual void slot_6c();
 virtual void slot_70();
 virtual void slot_74();
 virtual void slot_78();
 virtual void slot_7c();
 virtual void slot_80();
 virtual void slot_84();
 virtual void slot_88();
 virtual int Find(const void* key);
};
struct S004eee_Factory { S004eee_Controller* FUN_00537bd0(); };
struct S004eee_Anim { int FUN_0043b1b0(); };
struct S004eee_Entry20 {
 unsigned int unk00,unk04,unk08,unk0c,unk10;
 S004eee_Anim* FUN_006815c0();
};
struct S004eee_Entry16Sub {unsigned int unk00; void FUN_0066b0d0(int);};
struct S004eee_Entry16 {
 unsigned int unk00; S004eee_Entry16Sub m_sub04; unsigned int unk08; unsigned char unk0c; unsigned char unk0d; unsigned char unk0e; unsigned char unk0f;
};
extern unsigned char DAT_01096968;
struct S004eee_Owner {
 unsigned int unk00;
 unsigned int unk04;
 unsigned int unk08;
 unsigned int m_count;
 unsigned int unk10;
 S004eee_Entry16* m_dest;
 S004eee_Entry20* m_source;
 unsigned int unk1c;
 unsigned int unk20;
 unsigned int unk24;
 unsigned int unk28;
 unsigned int unk2c;
 unsigned int unk30;
 unsigned int unk34;
 unsigned int unk38;
 unsigned int unk3c;
 S004eee_Factory* m_factory;
 unsigned int unk44;
 unsigned int unk48;
 unsigned int unk4c;
 unsigned int unk50;
 unsigned int unk54;
 unsigned int unk58;
 unsigned int m_priorHandle;
 unsigned int m_handle;
 void FUN_004eee00();
};
void S004eee_Owner::FUN_004eee00() {
 S004eee_Controller* manager = m_factory->FUN_00537bd0();
 S004eee_Controller* cachedManager = manager;
 if (m_handle != 0) m_handle = manager->Find(&m_priorHandle);
 for (unsigned int i = 0; i < m_count; ++i) {
   S004eee_Entry20* entry = &m_source[i];
   int active = entry->FUN_006815c0()->FUN_0043b1b0();
   if (active == 0 || cachedManager->Find(entry->FUN_006815c0()) == 0) {
     m_dest[i].m_sub04.FUN_0066b0d0(0);
     m_dest[i].unk08 = 0;
     m_dest[i].unk0c = DAT_01096968;
   }
 }
}