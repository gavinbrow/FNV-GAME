
extern GraphicsSystem* DAT_011fe1e8;
extern GraphicsSystem* DAT_011fe1ec;
extern GraphicsResource* DAT_011fddc8;
extern GraphicsResource* DAT_011fdabc;
extern GraphicsResource* DAT_011fde44;
extern unsigned int DAT_011f9534;
extern unsigned int DAT_011f9538;
extern unsigned int DAT_011f950c;
extern unsigned int DAT_011fce70, DAT_011fc290, DAT_011fce74, DAT_011fc294;

void __cdecl FUN_00be7420()
{
    ScopedSystem system;
    ScopedTemporary temporary;
    system.reset(DAT_011fe1e8);

    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);

        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 3, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f9534;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);

        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 3, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f9538;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);

        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f950c;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);
    }
    system->material5c = DAT_011fddc8;
    system->material44 = DAT_011fdabc;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 4, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 1, 1);
    DAT_011fce70 = 128;
    DAT_011fc290 = 12;

    system.resetFromGlobal(DAT_011fe1ec);
    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 3, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f9534;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 3, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f9538;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        *(unsigned int*)((char*)temporary.ptr + 8) = DAT_011f950c;
        system->FUN_00e802b0(system->device14, (unsigned int)temporary.ptr);
    }
    system->material5c = DAT_011fde44;
    system->material44 = DAT_011fdabc;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 4, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 1, 1);
    DAT_011fce74 = 0x880;
    DAT_011fc294 = 12;
}
