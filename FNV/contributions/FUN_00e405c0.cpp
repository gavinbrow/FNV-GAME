extern float _DAT_0104da48;

float __cdecl FUN_00e405c0(int *param_1)
{
    float *pfVar1;
    int iVar2;
    int iVar3;
    int iVar4;
    float fStack_4;
    float fTemp;

    fStack_4 = _DAT_0104da48;
    iVar3 = param_1[1];
    iVar4 = 0;
    if (iVar3 >= 4) {
        pfVar1 = (float *)(param_1[0] + 8);
        iVar2 = (iVar3 - 4U >> 2) + 1;
        iVar4 = iVar2 * 4;
        do {
            fTemp = pfVar1[-2];
            if (fStack_4 < fTemp) { } else { fStack_4 = fTemp; }
            fTemp = pfVar1[-1];
            if (fStack_4 < fTemp) { } else { fStack_4 = fTemp; }
            fTemp = *pfVar1;
            if (fStack_4 < fTemp) { } else { fStack_4 = fTemp; }
            fTemp = pfVar1[1];
            if (fStack_4 < fTemp) { } else { fStack_4 = fTemp; }
            pfVar1 = pfVar1 + 4;
            iVar2 = iVar2 + -1;
        } while (iVar2 != 0);
    }
    if (iVar4 < iVar3) {
        pfVar1 = (float *)(param_1[0] + iVar4 * 4);
        iVar3 = iVar3 - iVar4;
        do {
            fTemp = *pfVar1;
            if (fStack_4 < fTemp) { } else { fStack_4 = fTemp; }
            pfVar1 = pfVar1 + 1;
            iVar3 = iVar3 + -1;
        } while (iVar3 != 0);
    }
    return fStack_4;
}