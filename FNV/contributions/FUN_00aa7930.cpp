// @fnv 0x00aa7930
class AbstractHeap { public: void Clear(); };
class __declspec(novtable) Heap00aaa5b0 {
public:
    virtual void Dummy() = 0;
    void FUN_00aa8da0();
    __forceinline ~Heap00aaa5b0() { FUN_00aa8da0(); }
};
class FUN_00aa7930_class : public Heap00aaa5b0 {
public:
    unsigned char pad[0x20ed];
    unsigned char active;
    virtual void Dummy();
    ~FUN_00aa7930_class();
};
FUN_00aa7930_class::~FUN_00aa7930_class()
{
    reinterpret_cast<AbstractHeap*>(this)->Clear();
    active = 1;
}