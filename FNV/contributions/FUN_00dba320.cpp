struct CallTarget_00dba270 { int FUN_00dba270(int, int, int, int, int); };
struct SearchObject {
    int FUN_00dba320(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3);
};
int SearchObject::FUN_00dba320(unsigned int arg0, unsigned int arg1, unsigned int arg2, unsigned int arg3)
{
    unsigned int callResult0 = (unsigned int)((CallTarget_00dba270*)this)->FUN_00dba270((int)arg0, (int)arg1, (int)0u, (int)arg2, (int)arg3);
    return (int)callResult0;
}
