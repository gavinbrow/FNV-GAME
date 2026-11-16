unsigned char FUN_005accb0(int param_1, int param_2, int param_3, int param_4,
                  int param_5, int param_6, int param_7, int* param_8);
void FUN_005de2c0(unsigned short param_1);

bool FUN_005de250(int param_1, int param_2, int param_3, int param_4,
                  int param_5, int param_6, int param_7, int param_8)
{
    int uStack_8 = 0;
    if (FUN_005accb0(param_1, param_2, param_8, param_3, param_4,
                     param_5, param_6, &uStack_8) == 0) {
        return false;
    }
    if (uStack_8 < 0 || uStack_8 > 0xffff) {
        return false;
    }
    FUN_005de2c0((unsigned short)uStack_8);
    return true;
}
