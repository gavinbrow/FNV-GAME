struct DeviceCallback { int unk00; int m_total; int (__cdecl *m_callback)(DeviceCallback*, void*, int, int*, int); __forceinline void Process(void* p) { int size=4; m_total+=m_callback(this,p,4,&size,1); } };
struct Resource { void FUN_00c905b0(); };
struct DeviceOwner; struct DeviceSubobject { void FUN_00d21ce0(DeviceOwner*); };
struct DeviceOwner { int unk00,unk04,unk08,unk0c; DeviceSubobject m_subobject; int unk14,unk18,m_payload; void FUN_00ca9b40(Resource*); };
struct InputObject {DeviceCallback* GetCallback() const {return *reinterpret_cast<DeviceCallback* const*>(reinterpret_cast<const char*>(this)+0x24c);}};
Resource* __cdecl FUN_00cf4af0(InputObject*);
struct FUN_00ca9ce0_class {int unk00; DeviceOwner* m_owner; void FUN_00c8a230(InputObject*); void FUN_00ca9ce0(InputObject*);};
void FUN_00ca9ce0_class::FUN_00ca9ce0(InputObject* input) {
 FUN_00c8a230(input); DeviceOwner* owner=m_owner; Resource* resource=FUN_00cf4af0(input);
 owner->FUN_00ca9b40(resource); owner->m_subobject.FUN_00d21ce0(owner); resource->FUN_00c905b0();
 DeviceCallback* callback=input->GetCallback(); callback->Process(&owner->m_payload);
}