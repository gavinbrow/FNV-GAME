struct CallTarget_00d5ed80 { int FUN_00d5ed80(int, int, int, int); };
struct SearchObject {
    int FUN_00d5eda0(unsigned int arg0, unsigned int arg1, unsigned int arg2);
};
int SearchObject::FUN_00d5eda0(unsigned int arg0, unsigned int arg1, unsigned int arg2)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00d5ed80*)this)->FUN_00d5ed80((int)arg0, (int)arg1, (int)arg2, (int)1u);
    return (int)callResult0;
}
