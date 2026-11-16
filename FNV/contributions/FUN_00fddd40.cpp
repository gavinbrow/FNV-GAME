struct Obj_01267b54 { void* m_vtbl; void FUN_00cbf1a0(); };
extern Obj_01267b54 DAT_01267b54;
extern char DAT_010c3af8[];
extern "C" void __cdecl FUN_00fddd40(void)
{
    DAT_01267b54.m_vtbl = DAT_010c3af8;
    DAT_01267b54.FUN_00cbf1a0();
}
