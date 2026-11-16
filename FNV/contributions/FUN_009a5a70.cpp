struct ItemList { unsigned int GetCount(); void QueryItem(void** result); };
struct SpawnedObject {
 int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c;
 SpawnedObject(); ~SpawnedObject();
 void Fill(void* item); void Attach(ItemList* list);
};
struct FUN_009a5a70_cls {
 void Dispatch(void* item, SpawnedObject* object);
 void FUN_009a5a70(ItemList* list);
};
void FUN_009a5a70_cls::FUN_009a5a70(ItemList* list) {
 unsigned int count = list->GetCount();
 for (unsigned int index = 0; index < count; ++index) {
 bool failed = false;
 SpawnedObject* object = new SpawnedObject;
 void* output;
 list->QueryItem(&output);
 object->Fill(output);
 object->Attach(list);
 if (output == 0) failed = true;
 if (!failed) Dispatch(output, object);
 else delete object;
 }
}