__declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
__declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern char* EmptyFS;
struct ValueHolder { void* m_owner; char* m_text; RefCounted* m_object; };
struct ObjectReference { RefCounted* m_object; };
void __stdcall FUN_00e8ded0(ValueHolder* destination, char** sourceText, ObjectReference incoming)
{
    char* text = *sourceText;
    if (destination->m_text != text) {
        if (text != EmptyFS) InterlockedIncrement((volatile long*)(text - 8));
        if (destination->m_text != EmptyFS) InterlockedDecrement((volatile long*)(destination->m_text - 8));
        destination->m_text = text;
    }
    RefCounted* previous = destination->m_object;
    if (previous != incoming.m_object) {
        if (previous && InterlockedDecrement(&previous->m_ref) == 0)
            previous->f1();
        destination->m_object = incoming.m_object;
        if (incoming.m_object) InterlockedIncrement(&incoming.m_object->m_ref);
    }
    if (incoming.m_object) {
        RefCounted* releasing = incoming.m_object;
        if (InterlockedDecrement(&releasing->m_ref) == 0)
            releasing->f1();
    }
}
