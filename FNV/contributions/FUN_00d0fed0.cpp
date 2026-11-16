struct TimeStep {float start,end,delta,inverse;};
struct World {
 TimeStep& time(){return *reinterpret_cast<TimeStep*>(reinterpret_cast<char*>(this)+80);}
};
struct Context {
 World*& world(){return *reinterpret_cast<World**>(reinterpret_cast<char*>(this)+120);}
 int& depth(){return *reinterpret_cast<int*>(reinterpret_cast<char*>(this)+148);}
 int& pending(){return *reinterpret_cast<int*>(reinterpret_cast<char*>(this)+140);}
 int& otherPending(){return *reinterpret_cast<int*>(reinterpret_cast<char*>(this)+144);}
 unsigned char& locked(){return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this)+156);}
 int& mode(){return *reinterpret_cast<int*>(reinterpret_cast<char*>(this)+164);}
 void FUN_00c91120();void FUN_00c91140();
};
struct Body { unsigned char& motion(){return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this)+232);} void* state(){return reinterpret_cast<char*>(this)+240;} };
void __cdecl FUN_00cf1b10(float,void*);
void __cdecl FUN_00d28680(TimeStep*,Body**,int,int);
void __cdecl FUN_00d1a330(World*,Body**,int);
struct Controller {
 virtual void slot0();virtual void slot1();virtual void slot2();virtual void slot3();virtual void slot4();virtual void slot5();virtual void slot6();virtual void slot7();virtual void process(Body**,int,Context*,int);
 int flags,kind,capacity,mode;float start,end;
 void FUN_00d0d3f0(Body**,int,Context*,int);
 void FUN_00d0f2e0(Body**,int,World*);
 void FUN_00d0fed0(Body**,int,Context*,int);
};
void Controller::FUN_00d0fed0(Body** bodies,int count,Context* context,int flags) {
 ++context->depth();
 World* world=context->world();
 float begin=start,finish=end;
 __declspec(align(16)) TimeStep saved=world->time();
 TimeStep step;step.start=begin;step.end=finish;step.delta=finish-begin;step.inverse=step.delta==0?0.0f:1.0f/step.delta;
 world->time()=step;
 int active=flags&1;
 if(active) {
 for(int i=0;i<count;++i) if(bodies[i]->motion()!=5) FUN_00cf1b10(start,bodies[i]->state());
 FUN_00d28680(&step,bodies,count,224);
 FUN_00d1a330(context->world(),bodies,count);
 }
 process(bodies,count,context,1);
 if(flags&2)FUN_00d0d3f0(bodies,count,context,0);
 if(flags&4)FUN_00d0f2e0(bodies,count,context->world());
 else if(active)process(bodies,count,context,2);
 if(--context->depth()==0&&!context->locked()) {
 if(context->pending())context->FUN_00c91120();
 if(context->mode()==1&&context->otherPending())context->FUN_00c91140();
 }
 context->world()->time()=saved;
}

