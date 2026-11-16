struct ArchivePtr { void *handle; };
extern ArchivePtr DAT_011f8190[9];
extern "C" void FUN_00afc720();
void __stdcall FUN_0065ee50_Helper(void*, unsigned int, int, void (__cdecl*)());
extern "C" void FUN_00fdc3c0() {
    FUN_0065ee50_Helper(DAT_011f8190, sizeof(ArchivePtr), 18, &FUN_00afc720);
}