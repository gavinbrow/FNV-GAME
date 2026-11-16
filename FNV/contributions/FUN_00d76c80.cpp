struct Target { float Call(int a, int b, int c); };
struct Owner { int unk00; int unk04; Target* unk08; void FUN_00d76c80(int a, int b, int c); };
void Owner::FUN_00d76c80(int a, int b, int c) { unk08->Call(a, b, c); }
