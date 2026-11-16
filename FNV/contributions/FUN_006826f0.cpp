void __cdecl FUN_00682740(void* data);

struct FUN_006826f0 {
    void* payload;
    unsigned int unknown04;
    FUN_006826f0* next;
    ~FUN_006826f0();
};

FUN_006826f0::~FUN_006826f0()
{
    FUN_00682740(payload);
    delete next;
}