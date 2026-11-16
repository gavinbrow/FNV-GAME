struct WorkerIface {
    virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3();
    virtual void v4(); virtual void v5(); virtual void v6(); virtual void v7();
    virtual void v8(); virtual void v9(void*);
};
struct Worker {
    int a, b, c;
    WorkerIface* p1;
    WorkerIface* p2;
    void __thiscall FUN_00d45270(void* value);
};
void Worker::FUN_00d45270(void* value) {
    p1->v9(value);
    if (p2) p2->v9(value);
}


