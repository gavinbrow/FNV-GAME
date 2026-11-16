struct CallTarget_00d5a410 { int FUN_00d5a410(int, int, int, int, int); };
struct SearchObject {
    int FUN_00d5a4c0(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3);
};
int SearchObject::FUN_00d5a4c0(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00d5a410*)this)->FUN_00d5a410((int)arg0, (int)arg1, (int)0u, (int)arg2, (int)arg3);
    return (int)callResult0;
}
