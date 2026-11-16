struct FUN_00e94150_Node {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    FUN_00e94150_Node* m_3c;
    FUN_00e94150_Node* m_40;
};

struct FUN_00e94150_Class {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    FUN_00e94150_Node* m_2c;

    void __thiscall FUN_00e94150(FUN_00e94150_Node* node);
};

void __thiscall FUN_00e94150_Class::FUN_00e94150(FUN_00e94150_Node* node)
{
    FUN_00e94150_Node* current = m_2c;

    if (current) {
        while (current) {
            if (current == node) {
                break;
            }

            current = current->m_3c;
            if (!current) {
                return;
            }
        }

        if (current->m_3c) {
            current->m_3c->m_40 = current->m_40;
        }

        if (current->m_40) {
            current->m_40->m_3c = current->m_3c;
        }

        if (current == m_2c) {
            m_2c = current->m_3c;
        }
    }
}