struct VirtualElement {virtual void v0(); virtual void v1(); virtual void v2(); virtual int v3();};
struct StateObject {VirtualElement* FUN_00933810();};
struct OwnerObject {StateObject* FUN_009306d0(); bool FUN_009337b0();};
bool OwnerObject::FUN_009337b0(){ StateObject* pointer; bool result = false; pointer = FUN_009306d0(); if (pointer && pointer->FUN_00933810()) { if (pointer->FUN_00933810()->v3() == 2) { result = true; } } return result; }