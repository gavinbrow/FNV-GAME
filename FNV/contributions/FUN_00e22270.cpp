struct VecData;
struct Components { int x,y,z,w; void copy(const VecData* from); };
struct VecData { int unk00,unk04,unk08,unk0c,x,y,z,w; };
inline void Components::copy(const VecData* from) { x=from->x; y=from->y; z=from->z; w=from->w; }
struct VectorGroup { int unk00,unk04; VecData* first; VecData* second; VecData* third; };
struct InputPacket { int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c; VectorGroup* group; };
struct Triple { Components first,second,third; };
int __cdecl FUN_00deab10(void*,const Triple*);
struct FUN_00e22270_Class { int unk00; unsigned int flags; int unk08,unk0c,output; float FUN_00e22270(InputPacket*); };
float FUN_00e22270_Class::FUN_00e22270(InputPacket* input) {
 __declspec(align(16)) Triple values;
 VectorGroup* group=input->group;
 values.first.copy(group->first);
 values.second.copy(group->second);
 values.third.copy(group->third);
 flags |= !!FUN_00deab10(&output,&values);
 volatile float outcome;
 if(flags) outcome=0.0f; else outcome=1.0f;
 return outcome;
}