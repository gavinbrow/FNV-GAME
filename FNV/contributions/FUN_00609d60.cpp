struct FUN_00609d60_shell : public TESNPC {
    void FUN_00609d60(int);
};

void FUN_00609d60_shell::FUN_00609d60(int unused)
{
    unsigned int i2 = 0;
    for (; i2 < 2; ++i2) {
        unsigned int j = 0;
        for (; j < 2; ++j) {
            unsigned int rows = this->RaceFaceOffsetCoord[i2][j].FUN_009611e0();
            unsigned int cols = this->RaceFaceOffsetCoord[i2][j].FUN_00441110();
            unsigned int row = 0;
            for (; row < rows; ++row) {
                unsigned int col = 0;
                for (; col < cols; ++col) {
                    float value = *this->RaceFaceOffsetCoord[i2][j].FUN_0060b370(row, col).FUN_00629ab0();
                    ((PC7d*)this)->FUN_00484ce0((unsigned int)&value, 4);
                }
            }
        }
    }
    int hairID = 0;
    if (this->GetFormRace() != 0) {
        hairID = (int)this->GetFormRace()->GetFormID();
    }
    ((FUN_00484d20_Class*)this)->FUN_00484d20(&hairID, 4);
    int raceID = 0;
    if (this->pHair != 0) {
        raceID = (int)this->pHair->GetFormID();
    }
    ((FUN_00484d20_Class*)this)->FUN_00484d20(&raceID, 4);
    int eyeID = 0;
    if (this->pEyeColor != 0) {
        eyeID = (int)this->pEyeColor->GetFormID();
    }
    ((FUN_00484d20_Class*)this)->FUN_00484d20(&eyeID, 4);
    ((PC7d*)this)->FUN_00484ce0((unsigned int)&this->fHairLength, 4);
    ((PC7d*)this)->FUN_00484ce0((unsigned int)&this->iHairColor, 4);
    unsigned char sex = 0;
    if (this->GetSex() == 1) {
        sex = 1;
    }
    ((PC7d*)this)->FUN_00484ce0((unsigned int)&sex, 1);
}

