void __cdecl FUN_00cebf30(float *param_1, float param_2, float *param_3)
{
    float fVar1;
    *param_3 = *param_3 + param_2 * (param_1[1] * param_1[1] + param_1[2] * param_1[2]);
    param_3[5] = (param_1[0] * param_1[0] + param_1[2] * param_1[2]) * param_2 + param_3[5];
    param_3[10] = (param_1[0] * param_1[0] + param_1[1] * param_1[1]) * param_2 + param_3[10];
    fVar1 = param_3[1] - param_1[0] * param_2 * param_1[1];
    param_3[1] = fVar1;
    param_3[4] = fVar1;
    fVar1 = param_3[6] - param_1[1] * param_2 * param_1[2];
    param_3[6] = fVar1;
    param_3[9] = fVar1;
    fVar1 = param_3[8] - param_1[0] * (param_1[2] * param_2);
    param_3[8] = fVar1;
    param_3[2] = fVar1;
}