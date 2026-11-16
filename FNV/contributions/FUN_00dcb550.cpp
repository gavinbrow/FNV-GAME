struct Entry { unsigned key; unsigned value; unsigned flags; unsigned type; unsigned state; unsigned metadata; };
struct Node {
 virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3(); virtual void slot4(); virtual void slot5(); virtual void slot6(); virtual void slot7(); virtual void slot8(); virtual int BaseIndex(); virtual void slot10(); virtual int Find(unsigned key);
 unsigned flags, type, state, metadata, level;
 Node* parent;
 unsigned capacity, size, reserved;
 Entry* entries;
 int count;
};
struct Object { virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3(); virtual void SetContext(void*); };
struct Item { unsigned key; Object* object; };
struct FUN_00dcb550_class {
 virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3(); virtual void slot4(); virtual void* Context();
 unsigned flags, count;
 Item* items;
 unsigned capacity, version;
 Node* current;
 int FUN_00dc9c20(Entry*);
 int FUN_00dcb550(unsigned key);
};
int FUN_00dcb550_class::FUN_00dcb550(unsigned key) {
 int offset = current->Find(key);
 Node* node = current;
 offset -= node->BaseIndex();
 Node* walk = node;
 Entry* entry;
 do {
  offset += walk->count;
  if (offset >= 0) goto found;
  walk = walk->parent;
 } while (walk);
 entry = node->entries - 1;
 goto resolve;
found:
 entry = &walk->entries[offset];
resolve:
 int index = FUN_00dc9c20(entry);
 if (index != -1) {
  Item* item = &items[index];
  item->object->SetContext(Context());
 }
 return index;
}


