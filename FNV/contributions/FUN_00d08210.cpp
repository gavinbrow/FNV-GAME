struct FUN_00d08210_Entry { void* collisionAgent; unsigned short collisionIndices[2]; unsigned int metadata08, metadata0C, metadata10; hkpLinkedCollidable* owner; };
struct FUN_00d08210_Pair { FUN_00d08210_Entry* entry; unsigned int key; };
int __cdecl FUN_00d081f0(const FUN_00d08210_Pair*, const FUN_00d08210_Pair*);
void __cdecl FUN_00d04200(FUN_00d08210_Pair*,int,int,int (__cdecl*)(const FUN_00d08210_Pair*,const FUN_00d08210_Pair*));
struct FUN_00d08210_Collidable : hkpLinkedCollidable { void FUN_00d08210(); };
void FUN_00d08210_Collidable::FUN_00d08210() {
 if(m_collisionEntries.m_size>1) FUN_00d04200((FUN_00d08210_Pair*)m_collisionEntries.m_data,0,m_collisionEntries.m_size-1,FUN_00d081f0);
 for(int index=0; index<m_collisionEntries.m_size; ++index) {
   volatile FUN_00d08210_Pair* pair = ((volatile FUN_00d08210_Pair*)m_collisionEntries.m_data)+index;
   FUN_00d08210_Entry* entry = pair->entry;
   entry->collisionIndices[this==entry->owner]=(unsigned short)index;
 }
}