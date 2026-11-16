struct LinkedEntry { int unk00; int value; int unk08; LinkedEntry* next; };

int FUN_00cf0860(int* output, int capacity, LinkedEntry* head) {
    LinkedEntry* entries[8];
    LinkedEntry* current = head;
    int count = 0;
    while (current->next) {
        entries[count] = current;
        current = current->next;
        ++count;
    }

    int written = 0;
    if (count > 0) {
        int limit = capacity - 1;
        do {
            if (written >= limit)
                break;
            --count;
            output[written] = entries[count]->value;
            ++written;
        } while (count > 0);
    }    output[written] = -1;
    return written + 1;
}

