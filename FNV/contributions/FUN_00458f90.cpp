struct FUN_00458f90_shell {
    void FUN_00458f90();
};
struct G2List : G2 {
    void FUN_00470470();
};

void FUN_00458f90_shell::FUN_00458f90()
{
    G2* entry = (G2*)((char*)this + 0x9c);
    while (entry != 0 && *entry->_ref_006815c0() != 0) {
        int* object = *entry->_ref_006815c0();
        delete object;
        entry = (G2*)entry->_ref_00726070();
    }
    ((G2List*)((char*)this + 0x9c))->FUN_00470470();
}