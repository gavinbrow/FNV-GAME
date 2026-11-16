struct DCAAObject { virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3(); virtual void* getKey(); };
struct DCAAMapEntry { DCAAObject* value; int next; };
struct DCAAMap { DCAAMapEntry* entries; int __thiscall FUN_00dc8e30(void* key); void __thiscall FUN_00dcb4b0(void* key,int index); void __thiscall FUN_00dc9ec0(void* key,DCAAObject** value); };
struct DCAAOwner { int unk00,unk04,unk08,unk0c; DCAAMap table; void __thiscall FUN_00dcaaf0(void* volatile key,DCAAObject* object); };
void DCAAOwner::FUN_00dcaaf0(void* volatile key,DCAAObject* object) {
    DCAAObject* savedObject=object; void* heldKey=key;
    if(heldKey) {
        int index=table.FUN_00dc8e30(heldKey);
        while(index!=-1) {
            if(table.entries[index].value==savedObject) {table.FUN_00dcb4b0(heldKey,index);break;}
            index=table.entries[index].next;
        }
    }
    void* nextKey=savedObject->getKey();
    if(nextKey) table.FUN_00dc9ec0(nextKey,&object);
}