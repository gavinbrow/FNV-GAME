struct FUN_00cebe80_Struct
{
    float unk00;
    float unk04;
    float unk08;
};

void __cdecl FUN_00cebe80(FUN_00cebe80_Struct *pThis, float fParam2, float *pOut)
{
    float temp;

    temp = pOut[0] - fParam2 * (pThis->unk08 * pThis->unk08 + pThis->unk04 * pThis->unk04);
    pOut[0] = temp;

    temp = pOut[5] - fParam2 * (pThis->unk00 * pThis->unk00 + pThis->unk08 * pThis->unk08);
    pOut[5] = temp;

    temp = pOut[10] - fParam2 * (pThis->unk00 * pThis->unk00 + pThis->unk04 * pThis->unk04);
    pOut[10] = temp;

    temp = pThis->unk00 * fParam2 * pThis->unk04 + pOut[1];
    pOut[1] = temp;
    pOut[4] = temp;

    temp = fParam2 * pThis->unk04 * pThis->unk08 + pOut[6];
    pOut[6] = temp;
    pOut[9] = temp;

    temp = fParam2 * pThis->unk08 * pThis->unk00 + pOut[8];
    pOut[8] = temp;
    pOut[2] = temp;
}
