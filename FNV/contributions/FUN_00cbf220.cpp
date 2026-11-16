struct Visitor {
    virtual void slot00();
    virtual void slot04();
    virtual void Visit(void* item, int arg);
    void FUN_00cbf220(void** items, int count, int arg);
};

void Visitor::FUN_00cbf220(void** items, int count, int arg)
{
    int i = 0;
    if (0 < count) {
        do {
            void* item = items[i];
            if (item != 0) {
                Visit(item, arg);
            }
            i = i + 1;
        } while (i < count);
    }
}
