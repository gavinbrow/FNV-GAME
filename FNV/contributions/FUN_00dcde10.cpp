void* __cdecl FUN_00cb1260(void*, const void*, unsigned int);
void* __cdecl FUN_00d32ac0(void*, void*);
int __cdecl FUN_00dcd950(void*, void*, void*);
int FUN_00dcd4d0(void* p) {
 if(p==reinterpret_cast<void*>(&FUN_00d3fe90)) return 1;
 if(p==reinterpret_cast<void*>(&FUN_00d39390)) return 2;
 if(p==reinterpret_cast<void*>(&FUN_00d41a30)) return 3;
 if(p==reinterpret_cast<void*>(&FUN_00d40d80)) return 4;
 if(p==reinterpret_cast<void*>(&FUN_00d32cd0)) return 5;
 if(p==reinterpret_cast<void*>(&FUN_00da6eb0)) return 6;
 if(p==reinterpret_cast<void*>(&FUN_00d2d890)) return 7;
 if(p==reinterpret_cast<void*>(&FUN_00d35770)) return 8;
 if(p==reinterpret_cast<void*>(&FUN_00d365d0)) return 9;
 return 0;
}
struct EntryState { unsigned int count, capacity, flags; };
__forceinline EntryState* reset(EntryState* p) { if(p) {p->count=0;p->capacity=0;p->flags=0x80000000;} return p; }
int FUN_00dcde10(char* source, int kind, void* context, char** registry, unsigned char* instruction) {
 unsigned char* payload;
 switch(instruction[0]) {case 2: payload=instruction+32;break;case 4:payload=instruction+48;break;case 6:return 1;default:return 1;}
 if(FUN_00dcd4d0(*reinterpret_cast<void**>(*registry+0x16dc+instruction[1]*80))!=kind) return 1;
 switch(kind) {
 case 1:case 2:case 3:case 4:
 FUN_00cb1260(instruction+24, source+140,104);
 instruction[2]=source[118]; instruction[3]=source[119]; return 0;
 case 5:
 FUN_00cb1260(instruction+24, source+140,104);
 instruction[2]=source[118]; instruction[3]=source[119];
 if(payload[11]&32)return 0;
 return FUN_00dcd950(context,registry,reset(static_cast<EntryState*>(FUN_00d32ac0(instruction,payload))));
 case 6:case 7:case 8:case 9:
 FUN_00cb1260(instruction+24,source+140,104);
 return FUN_00dcd950(context,registry,reset(reinterpret_cast<EntryState*>(payload)));
 default:return 1;
 }
}

