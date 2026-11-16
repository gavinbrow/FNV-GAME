struct CallTarget_00a74e10 { int FUN_00a74e10(int, int); };
struct SearchObject {
    int FUN_00a755d0(unsigned int arg0);
};
int SearchObject::FUN_00a755d0(unsigned int arg0)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00a74e10*)this)->FUN_00a74e10((int)(arg0 + 220u), (int)(104u + arg0));
    return (int)callResult0;
}
