// Original synthetic component: compile/link only, never execute.
// Exercises compiler-generated RTTI and C++ exception metadata.
struct Base { virtual ~Base(); };
struct Derived : Base { virtual ~Derived(); };
Base::~Base() {}
Derived::~Derived() {}
__declspec(noinline) Derived* cast_value(Base* value) {
    return dynamic_cast<Derived*>(value);
}
__declspec(noinline) int catch_value(int value) {
    try { if (value) throw value; }
    catch (int caught) { return caught; }
    return 0;
}
int main(int argc, char**) {
    Derived value;
    Base* base = &value;
    return (cast_value(base) != 0) + catch_value(argc);
}
