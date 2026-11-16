extern __declspec(thread) unsigned int threadContext;
inline unsigned int& currentAllocationMode() {
    return *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(&threadContext) + 0x2b4);
}

class ScopedAllocationMode {
    unsigned int previous;
public:
    ScopedAllocationMode() : previous(currentAllocationMode()) { currentAllocationMode() = 16; }
    ~ScopedAllocationMode() { currentAllocationMode() = previous; }
};

class ObjectCandidate {
public:
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual void slot6();
    virtual void slot7();
    virtual void slot8();
    virtual void slot9();
    virtual void slot10();
    virtual void slot11();
    virtual void slot12();
    virtual void slot13();
    virtual void slot14();
    virtual void slot15();
    virtual void slot16();
    virtual void slot17();
    virtual void slot18();
    virtual void slot19();
    virtual void slot20();
    virtual void slot21();
    virtual void slot22();
    virtual void slot23();
    virtual void slot24();
    virtual void slot25();
    virtual void slot26();
    virtual void slot27();
    virtual void slot28();
    virtual void slot29();
    virtual void slot30();
    virtual void slot31();
    virtual void slot32();
    virtual void slot33();
    virtual void slot34();
    virtual void slot35();
    virtual void slot36();
    virtual int QueryValue();
    virtual void slot38();
    virtual void slot39();
    virtual void Reset();
    int unk04;
    int activeObject;
    bool FUN_00c86ab0(class Item* item);
    void FUN_00c86940(Item*);
};
class Item {
public:
    int unk00;
    int unk04;
    int matchingValue;
    void FUN_00c6b3c0(int);
};
bool ObjectCandidate::FUN_00c86ab0(Item* item) {
    ScopedAllocationMode guard;
    int current = this ? activeObject : 0;
    bool result = false;
    if (current != 0) {
        if (item) {
            if (QueryValue() != item->matchingValue) {
                Reset();
                FUN_00c86940(item);
                item->FUN_00c6b3c0(current);
                result = true;
            }
        } else {
            Reset();
        }
    }
    return result;
}