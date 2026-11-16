struct TESObjectDoorController {
 static void* operator new(unsigned int);
 static void operator delete(void*);
 TESObjectDoorController();
 void* vtable; unsigned int references; void* next; unsigned short flags; unsigned short state; float frequency; float phase; float startTime; float stopTime; float lastTime; float weightedTime; float scaledTime; void* target; void* interpolation; void* door; void* animation;
};
struct ControllerFactory { void FUN_008d17d0(TESObjectDoorController*,void*); TESObjectDoorController* FUN_008d1740(void*); };
TESObjectDoorController* ControllerFactory::FUN_008d1740(void* context) {
 TESObjectDoorController* result=new TESObjectDoorController;
 FUN_008d17d0(result,context);
 return result;
}
