struct PhantomListeners : hkpPhantom {
    void __thiscall FUN_00d07c10(void* listener);
};
void PhantomListeners::FUN_00d07c10(void* listener) {
    int foundIndex;
    int index = 0;
    int count = m_phantomListeners.m_size;
    if (count > 0) {
        void** current = m_phantomListeners.m_data;
        do {
            if (*current == listener) {
                foundIndex = index;
                goto found;
            }
            ++index;
            ++current;
        } while (index < count);
    }
    foundIndex = -1;
found:
    --(volatile int&)m_phantomListeners.m_size;
    int bytes = ((volatile int&)m_phantomListeners.m_size - foundIndex) * 4;
    void** destination = m_phantomListeners.m_data + foundIndex;
    void** source = destination + 1;
    for (int offset = 0; offset < bytes; offset += 4) {
        *(void**)((char*)destination + offset) = *(void**)((char*)source + offset);
    }
}