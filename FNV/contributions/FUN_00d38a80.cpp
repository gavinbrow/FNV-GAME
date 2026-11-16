struct CallbackState {
    const void* type;
    bool completed;
    unsigned context;
};

extern const unsigned vtable_010ce81c[];

struct Operation {
    void FUN_00d37ed0(unsigned second, unsigned first,
                      unsigned third, CallbackState* callback);
    void FUN_00d38a80(unsigned first, unsigned second,
                      unsigned third, unsigned context);
};

void Operation::FUN_00d38a80(unsigned first, unsigned second,
                           unsigned third, unsigned context)
{
    CallbackState callback;
    callback.context = context;
    callback.completed = false;
    callback.type = vtable_010ce81c;
    FUN_00d37ed0(second, first, third, &callback);
}
