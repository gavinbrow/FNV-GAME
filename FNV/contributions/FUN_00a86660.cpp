extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long* value);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);

struct RefCountedObject {
    virtual void UnknownVirtual();
    virtual void DeleteThis();
    volatile long referenceCount;
};

struct CloneObject {
    int unk00;
    int unk04;
    RefCountedObject* first;
    RefCountedObject* second;

    void FUN_00a5d450(CloneObject* destination, void* process);
    void FUN_00a86660(CloneObject* destination, void* process);
};

void CloneObject::FUN_00a86660(CloneObject* destination, void* process)
{
    FUN_00a5d450(destination, process);

    RefCountedObject* previous = destination->first;
    if (previous != first) {
        if (previous && InterlockedDecrement(&previous->referenceCount) == 0) {
            previous->DeleteThis();
        }
        RefCountedObject* replacement = first;
        destination->first = replacement;
        if (replacement) {
            InterlockedIncrement(&replacement->referenceCount);
        }
    }

    previous = destination->second;
    if (previous != second) {
        if (previous && InterlockedDecrement(&previous->referenceCount) == 0) {
            previous->DeleteThis();
        }
        RefCountedObject* replacement = second;
        destination->second = replacement;
        if (replacement) {
            InterlockedIncrement(&replacement->referenceCount);
        }
    }
}