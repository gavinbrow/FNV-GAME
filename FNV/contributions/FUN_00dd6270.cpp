struct Arg {
    void* data;
    int count;
};

struct B {
    int f0;
    int f1;
    int f2;
    int f3;

    void* FUN_00d74d40();
};

struct A {
    int f0;
    int f1;
    int f2;
    int f3;
    int f4;

    void FUN_00d76ca0();
    int FUN_00d774a0(void*, int, void*);
    void FUN_00d76120(int, int);
    void FUN_00d76940();
};

int __cdecl FUN_00dd6270(Arg* a, int second) {
    if (a->count < 4) {
        return 1;
    }

    B objB;
    A objA;

    objA.FUN_00d76ca0();

    int count = a->count;
    void* data = a->data;

    void* q = objB.FUN_00d74d40();
    int r = objA.FUN_00d774a0(data, count, q);

    if (r != -1) {
        objA.FUN_00d76120(1, second);
        objA.FUN_00d76940();
        return 0;
    }

    objA.FUN_00d76940();
    return 1;
}
