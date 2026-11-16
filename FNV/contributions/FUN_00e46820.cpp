struct FnvDisabledCollisionFilter : hkpDisableEntityCollisionFilter {
    char* FUN_00e46820(char* wasRemoved, hkpEntity* entity);
};
char* FnvDisabledCollisionFilter::FUN_00e46820(char* wasRemoved, hkpEntity* entity) {
    if (!entity) {
        *wasRemoved = 0;
        return wasRemoved;
    }
    for (int index = 0; index < m_disabledEntities.m_size; ++index) {
        if (m_disabledEntities.m_data[index] == entity) {
            volatile int& count = m_disabledEntities.m_size;
            --count;
            int last = count;
            if (last != index)
                m_disabledEntities.m_data[index] = m_disabledEntities.m_data[last];
            *wasRemoved = 1;
            return wasRemoved;
        }
    }
    *wasRemoved = 0;
    return wasRemoved;
}