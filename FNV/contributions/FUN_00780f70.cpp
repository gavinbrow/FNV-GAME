struct InputInterface {
    virtual int Reserved0();
    virtual int Reserved1();
    virtual int GetFirstValue(int index);
    virtual int Reserved3();
    virtual int Reserved4();
    virtual int Reserved5();
    virtual int Reserved6();
    virtual int GetSecondValue(int index);
};
extern char* DAT_011dea3c;
bool __cdecl FUN_00780f70() {
    for (int index = 25; index < 31; ++index) {
        if (((InputInterface*)(DAT_011dea3c + 0xa4))->GetFirstValue(index) <
            ((InputInterface*)(DAT_011dea3c + 0xa4))->GetSecondValue(index)) {
            return true;
        }
    }
    return false;
}