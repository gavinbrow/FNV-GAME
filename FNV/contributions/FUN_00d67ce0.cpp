class PrimaryBase { public: virtual void primary0(); int flags; };
class ProcessBase { public: virtual void process0(); virtual void process1(); virtual void process2(); virtual void process3(); virtual void process4(); virtual void process5(); virtual void process6(); int unk04, unk08, unk0C, unk10, unk14; };
class WorldListener { public: virtual void world0(); virtual void world1(); virtual void world2(); int unk04; };
class FUN_00ddccb0 : public PrimaryBase, public ProcessBase, public WorldListener { public: FUN_00ddccb0(int); };
class hkpContactListener { public: virtual void contact0(); virtual void contact1(); virtual void contact2(); };
class hkpWorldPostSimulationListener { public: virtual void post0(); virtual void post1(); virtual void post2(); };
class hkpEntityListener { public: virtual void entity0(); virtual void entity1(); virtual void entity2(); virtual void entity3(); virtual void entity4(); virtual void entity5(); };
struct CountArray { int* data; int size; int capacity; CountArray() : data(0), size(0), capacity(-1) {} void FUN_00cb1fe0(void*, int); };
struct BSAudio { int unk00,unk04,unk08,unk0C; void* allocator; };
BSAudio* FUN_00c85750();
class FUN_00d67ce0 : public FUN_00ddccb0, public hkpContactListener, public hkpWorldPostSimulationListener, public hkpEntityListener
{
public:
    virtual void primary0(); virtual void primary1(); virtual void primary2();
    virtual void process0(); virtual void process1(); virtual void process2(); virtual void process3(); virtual void process4(); virtual void process5(); virtual void process6();
    virtual void world0(); virtual void world1(); virtual void world2();
    virtual void contact0(); virtual void contact1(); virtual void contact2();
    virtual void post0(); virtual void post1(); virtual void post2();
    virtual void entity0(); virtual void entity1(); virtual void entity2(); virtual void entity3(); virtual void entity4(); virtual void entity5();
    CountArray counts;
    FUN_00d67ce0(int context);
};

FUN_00d67ce0::FUN_00d67ce0(int context) : FUN_00ddccb0(context) { BSAudio* audio = FUN_00c85750(); counts.FUN_00cb1fe0(audio->allocator, 0); }


