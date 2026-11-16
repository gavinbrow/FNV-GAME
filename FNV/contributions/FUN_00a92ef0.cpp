struct CallTarget_00a68c60 { int FUN_00a68c60(int); };
struct CallTarget_00a92c40 { int FUN_00a92c40(); };
struct SearchObject {
    int FUN_00a92ef0(unsigned int arg0);
};
int SearchObject::FUN_00a92ef0(unsigned int arg0)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00a68c60*)this)->FUN_00a68c60((int)arg0);
    unsigned int callResult1 = (unsigned int)((CallTarget_00a92c40*)this)->FUN_00a92c40();
    return (int)callResult1;
}
