struct FUN_00d60500 {
 virtual void placeholder();
 unsigned int capacity;
 unsigned int count;
 void* storage;
 void* owner;
 FUN_00d60500(void* parent, unsigned int requested);
};
FUN_00d60500::FUN_00d60500(void* parent, unsigned int requested) : owner(parent), count(0), storage(0) {
 if (!requested) { capacity = 0x20000; return; } capacity = requested;
}

