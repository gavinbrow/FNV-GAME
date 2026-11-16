struct CallbackInterface {
    virtual void __cdecl NotifyFirst();
    virtual int __cdecl NotifySecond();
};
struct CallbackOwner {
    void* userData;
    void* context;
    void* next;
    CallbackInterface* handler;
};
int __cdecl FUN_009fd410(CallbackOwner* owner) {
    return owner->handler->NotifySecond();
}