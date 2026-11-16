struct Target { void FUN_00d65970(); };
struct Adjustor { void FUN_00d65fb0(); };
void Adjustor::FUN_00d65fb0() {
    ((Target*)((char*)this - 0x20))->FUN_00d65970();
}
