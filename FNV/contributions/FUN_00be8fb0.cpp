extern GraphicsSystem* DAT_011fe908;
extern GraphicsSystem* DAT_011fe90c;
extern GraphicsSystem* DAT_011fe910;
extern GraphicsSystem* DAT_011fe914;
extern GraphicsResource* DAT_011fddd4;
extern GraphicsResource* DAT_011fde48;
extern GraphicsResource* DAT_011fdac8;
extern GraphicsResource* DAT_011fdacc;
extern unsigned int DAT_011fd58c;
extern unsigned int DAT_011fd590;
extern unsigned int DAT_011fd594;
extern unsigned int DAT_011fd598;
extern unsigned int DAT_011fc9ac;
extern unsigned int DAT_011fc9b0;
extern unsigned int DAT_011fc9b4;
extern unsigned int DAT_011fc9b8;
extern unsigned int DAT_011fb1ec;
extern unsigned int DAT_011fb1f0;
extern unsigned int DAT_011fb1f4;
extern unsigned int DAT_011fb1f8;

void __cdecl FUN_00be8fb0()
{
    ScopedSystem system;
    ScopedTemporary temporary;

    system.resetFromGlobal(DAT_011fe908);
    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
    }
    system->material5c = DAT_011fddd4;
    system->material44 = DAT_011fdac8;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(19, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(20, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 3, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 0, 1);
    DAT_011fd58c = 1028;
    DAT_011fc9ac = 36;
    DAT_011fb1ec = 4;

    system.resetFromGlobal(DAT_011fe90c);
    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
    }
    system->material5c = DAT_011fddd4;
    system->material44 = DAT_011fdacc;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(19, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(20, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 3, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 0, 1);
    DAT_011fd590 = 1028;
    DAT_011fc9b0 = 36;
    DAT_011fb1f0 = 4;

    system.resetFromGlobal(DAT_011fe910);
    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
    }
    system->material5c = DAT_011fde48;
    system->material44 = DAT_011fdac8;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(19, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(20, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 3, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 0, 1);
    DAT_011fd594 = 3076;
    DAT_011fc9b4 = 36;
    DAT_011fb1f4 = 4;

    system.resetFromGlobal(DAT_011fe914);
    if (system->GetVersion() < 4) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 2, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 3, 1, 2, 1);
        system->FUN_00e802b0(system->device14, reinterpret_cast<unsigned int>(temporary.ptr));
    }
    system->material5c = DAT_011fde48;
    system->material44 = DAT_011fdacc;
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(27, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(19, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(20, 2, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(15, 0, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(7, 1, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(23, 3, 1);
    if (!system->manager30) system->manager30 = FUN_00e7f5d0();
    system->manager30->FUN_00e7f430(14, 0, 1);
    DAT_011fd598 = 3076;
    DAT_011fc9b8 = 36;
    DAT_011fb1f8 = 4;
}
