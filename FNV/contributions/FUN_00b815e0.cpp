struct InputFlag {
    unsigned int unk00;
    unsigned int unk04;
    unsigned char enabled;
};

extern "C" InputFlag* DAT_011ff4a0;
extern "C" InputFlag* DAT_011ff4a4;
extern "C" InputFlag* DAT_011ff4a8;
extern "C" InputFlag* DAT_011ff4ac;
extern "C" InputFlag* DAT_011ff4b0;
extern "C" InputFlag* DAT_011ff4b4;
extern "C" InputFlag* DAT_011ff4b8;
extern "C" InputFlag* DAT_011ff4bc;
extern "C" InputFlag* DAT_011ff4c0;
extern "C" unsigned int DAT_011ff248[];
extern "C" unsigned int DAT_011ff120[];
extern "C" unsigned char DAT_011ff118;
extern "C" unsigned char DAT_011ff119;
extern "C" unsigned char DAT_011ff11a;
extern "C" unsigned char DAT_011ff110;
extern "C" unsigned char DAT_011ff111;
extern "C" unsigned char DAT_011ff112;
extern "C" unsigned char DAT_011ff113;
extern "C" unsigned char DAT_011ff114;
extern "C" unsigned char DAT_011ff115;

void __cdecl FUN_00b815e0(int index)
{
    if (DAT_011ff4a0)
        DAT_011ff4a0->enabled = 1;
    DAT_011ff118 = (DAT_011ff248[index] >> 1) & 1;

    if (DAT_011ff4a4)
        DAT_011ff4a4->enabled = 1;
    DAT_011ff119 = (DAT_011ff248[index] >> 2) & 1;

    if (DAT_011ff4a8)
        DAT_011ff4a8->enabled = 1;
    DAT_011ff11a = (DAT_011ff248[index] >> 3) & 1;

    if (DAT_011ff4ac)
        DAT_011ff4ac->enabled = (DAT_011ff120[index] >> 1) & 1;
    DAT_011ff110 = (DAT_011ff120[index] >> 1) & 1;

    if (DAT_011ff4b0)
        DAT_011ff4b0->enabled = (DAT_011ff120[index] >> 2) & 1;
    DAT_011ff111 = (DAT_011ff120[index] >> 2) & 1;

    if (DAT_011ff4b4)
        DAT_011ff4b4->enabled = (DAT_011ff120[index] >> 3) & 1;
    DAT_011ff112 = (DAT_011ff120[index] >> 3) & 1;

    if (DAT_011ff4b8)
        DAT_011ff4b8->enabled = (DAT_011ff120[index] >> 4) & 1;
    DAT_011ff113 = (DAT_011ff120[index] >> 4) & 1;

    if (DAT_011ff4bc)
        DAT_011ff4bc->enabled = (DAT_011ff120[index] >> 5) & 1;
    DAT_011ff114 = (DAT_011ff120[index] >> 5) & 1;

    if (DAT_011ff4c0)
        DAT_011ff4c0->enabled = (DAT_011ff120[index] >> 6) & 1;
    DAT_011ff115 = (DAT_011ff120[index] >> 6) & 1;
}