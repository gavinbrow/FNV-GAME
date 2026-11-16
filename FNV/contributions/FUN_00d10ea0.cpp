struct Entry {
    unsigned short key;
    unsigned short value;
};
Entry* __stdcall FUN_00d10ea0(Entry* first, Entry* last, unsigned short key) {
    while ((((char*)last - (char*)first) & ~3) > 0x40) {
        Entry* middle = first + (((char*)last - (char*)first) >> 3);
        if (middle->key < key) first = middle;
        else last = middle;
    }
    while (first->key < key) ++first;
    return first;
}