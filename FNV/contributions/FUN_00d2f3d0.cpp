struct CallTarget_00d2f760 { int FUN_00d2f760(int, int, int, int); };
struct SearchObject {
    int FUN_00d2f3d0(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3);
};
int SearchObject::FUN_00d2f3d0(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00d2f760*)this)->FUN_00d2f760((int)arg1, (int)arg0, (int)arg2, (int)arg3);
    return (int)callResult0;
}
