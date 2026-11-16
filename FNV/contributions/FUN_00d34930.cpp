extern int DAT_010ce81c;
void __cdecl FUN_00d33b90(int b, int a, int c, SpawnedBuf* buffer);
void __cdecl FUN_00d34930(int a, int b, int c, int d)
{
    SpawnedBuf buffer;
    buffer.m_4 = 0;
    buffer.m_0 = &DAT_010ce81c;
    buffer.m_8 = d;
    FUN_00d33b90(b, a, c, &buffer);
}