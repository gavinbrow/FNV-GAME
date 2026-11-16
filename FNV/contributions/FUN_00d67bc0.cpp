struct Item;
struct Sink { void FUN_00c9c670(Item*); };
struct Link { void FUN_00cb1fb0(Sink*); };
struct Item { int value; Link link; void FUN_00d67bc0(Sink*); };
struct Prefix { float x,y,z,w; float ax,ay,az,aw; float bx,by,bz,bw; };
struct Derived : Prefix, Item {};
void Item::FUN_00d67bc0(Sink* sink) { sink->FUN_00c9c670(static_cast<Item*>(reinterpret_cast<Derived*>(reinterpret_cast<char*>(this) - sizeof(Prefix)))); link.FUN_00cb1fb0(sink); }


