struct FUN_00b00ae0_class {
 virtual void virtual0(); virtual void virtual1(); virtual void virtual2(); virtual void virtual3(); virtual void virtual4(); virtual bool virtual5(void* value);
 bool enabled;
 bool __thiscall FUN_00b00ae0(void** value);
};
bool FUN_00b00ae0_class::FUN_00b00ae0(void** value) {
 bool flag = enabled;
 {
   void* current;
   {
     void* payload;
     return (flag && (current = *value)) ? virtual5(payload = *value) : false;
   }
 }
}