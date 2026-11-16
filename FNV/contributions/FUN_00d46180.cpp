struct CallTarget_00d45350 { int FUN_00d45350(int, int, int, int); };
struct SearchObject {
    int FUN_00d46180(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3);
};
int SearchObject::FUN_00d46180(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00d45350*)this)->FUN_00d45350((int)arg1, (int)arg0, (int)arg2, (int)arg3);
    return (int)callResult0;
}
