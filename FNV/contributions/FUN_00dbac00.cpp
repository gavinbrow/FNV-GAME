struct Target {
 virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3(); virtual void slot4(); virtual void Invoke();
};
struct Wrapper {
 Target* target;
 void FUN_00dbac00();
};
void Wrapper::FUN_00dbac00() { target->Invoke(); }
