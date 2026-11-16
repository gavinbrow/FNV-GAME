class C857370 {
public:
    int * __thiscall FUN_00857370(int *, int, int);
};
class C8578b0 {
public:
    void __thiscall FUN_008578b0(int *, int);
};
class C857950 {
public:
    void __thiscall FUN_00857950(int *a, int b);
};

void __cdecl FUN_00aff0b0(int);

void __thiscall C857950::FUN_00857950(int *a, int b)
{
    int *p;
    if (a == 0)
        return;
    p = ((C857370 *)this)->FUN_00857370(a, b, 3);
    if (p == 0)
        p = a;
    FUN_00aff0b0((*(int (__thiscall **)(int *))(*(int **)p + 6))(p));
    ((C8578b0 *)this)->FUN_008578b0(p, 3);
}