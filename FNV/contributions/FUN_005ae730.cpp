struct FUN_005ae730_shell {
 List* FUN_005a8080();
 void FUN_005ae730();
};
struct HairObject { void* FUN_0061cb30(unsigned int); };
void FUN_005ae730_shell::FUN_005ae730() {
 List* list = FUN_005a8080();
 while (list && !list->_ref_008256d0()) {
   HairObject* object;
   void* item = list->_ref_006815c0();
   object = static_cast<HairObject*>(item);
   object ? object->FUN_0061cb30(1) : 0;
   list->_ref_0063f7b0();
 }
}