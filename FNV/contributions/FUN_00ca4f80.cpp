struct Link {};
struct Header { int state; int flags; void* value; int type; Link link; };
struct Node { virtual void f00(); virtual void f04(); virtual void f08(); virtual void f0c(); virtual Link* get(); };
struct Sink { virtual void f00(); virtual void f04(); virtual void f08(); virtual void f0c(); virtual void f10(); virtual void f14(); virtual void f18(); virtual void f1c(); virtual void f20(); virtual void f24(); virtual void f28(); virtual void f2c(); virtual void set(void*); };
struct Owner { int state; int flags; Node* node; void FUN_00c84d50(Sink*); void FUN_00ca4f80(Sink*);
 void* getValue() { if (this) { Node* current=node; if (current) { Link* link=current->get(); if (link) { Header* header=reinterpret_cast<Header*>(reinterpret_cast<char*>(link)-16); if (header) return header->value; } } } return 0; }
};
void Owner::FUN_00ca4f80(Sink* sink) { sink->set(getValue()); FUN_00c84d50(sink); }

