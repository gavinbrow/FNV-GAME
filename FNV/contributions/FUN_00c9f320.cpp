__declspec(thread) int tlsMode = 0x3b;
struct ReleaseObject {
    void FUN_00c8f670(int value);
};
struct FUN_00c9f320_object {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    void FUN_00c9f320(char release);
};
struct TlsGuard {
    int previous;
    TlsGuard() {
        previous = tlsMode;
        tlsMode = 0x10;
    }
    ~TlsGuard() {
        tlsMode = previous;
    }
};
void FUN_00c9f320_object::FUN_00c9f320(char release) {
    TlsGuard guard;
    if (release) {
        ReleaseObject* object = (ReleaseObject*)unk0c;
        if (object) {
            object->FUN_00c8f670(1);
        }
        unk0c = 0;
    }
}