void __cdecl FUN_00d26230(void* first, void* second, void* third, float value, int last);
struct FUN_00d56040_shell { void __thiscall FUN_00d56040(void* first, float value, int last); };
void __thiscall FUN_00d56040_shell::FUN_00d56040(void* first, float value, int last)
{
    FUN_00d26230(first, (unsigned char*)this + 0x90, (unsigned char*)this + 0xa0, value, last);
}
