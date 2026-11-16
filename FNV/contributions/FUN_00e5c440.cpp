struct CallTarget_00e5c420 { int FUN_00e5c420(int, int, int, int); };
struct SearchObject {
    int FUN_00e5c440(unsigned int arg0, unsigned int arg1, unsigned int arg2);
};
int SearchObject::FUN_00e5c440(unsigned int arg0, unsigned int arg1, unsigned int arg2)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00e5c420*)this)->FUN_00e5c420((int)arg0, (int)arg1, (int)arg2, (int)1u);
    return (int)callResult0;
}
