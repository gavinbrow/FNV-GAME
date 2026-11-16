struct Quad { int a; int b; int c; int d; };
struct Block {
    Quad q0; Quad q1; Quad q2; Quad q3; Quad q4; Quad q5;
    int e0; int e1;
};
struct Entry {
    Block data;
    int unk68;
    char unk6c;
    char unk6d;
};
struct Flag { char v; };
struct Cls {
    Quad h0; Quad h1; Quad h2; Quad h3;
    Entry* cursor;
    Block current;
    char flag;
    void FUN_00e65040(Flag a, int b);
};
void Cls::FUN_00e65040(Flag a, int b) {
    Entry* e = cursor;
    e->unk6d = a.v;
    if (a.v) {
        e->unk68 = b;
    }
    e->unk6c = flag;
    e->data = current;
    cursor = cursor + 1;
}
