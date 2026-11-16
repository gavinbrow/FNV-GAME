struct A32 { unsigned int v:32; };
struct B3 { unsigned int a:20; unsigned int b:4; unsigned int c:8; };
extern A32 DAT_011f7258; extern B3 DAT_011f725c;
inline void setA(A32& s, unsigned v) { s.v = v; }
inline void setB(B3& s, unsigned a, unsigned b, unsigned c) { s.c = c; s.b = b; s.a = a; }
void FUN_00fb82a0() { setA(DAT_011f7258, 0); setB(DAT_011f725c, 0, 0, 1); }
