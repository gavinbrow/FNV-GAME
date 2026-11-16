struct State { bool status; State(){} };
struct Counters { int step; int base; int misc; int length; };
struct FUN_00d46ca0_Class { int unk00,unk04; Counters* counters; int position; State FUN_00d46ca0(); };
State FUN_00d46ca0_Class::FUN_00d46ca0() { State result; result.status = position <= (counters->length - 1)*counters->step + counters->base; return result; }