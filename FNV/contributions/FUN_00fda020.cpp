extern "C" void __cdecl FUN_00aa10f0(void*);
extern unsigned char DAT_01094e3c;
extern unsigned char DAT_01094e5c;
class ScrapListBase { public: void *vtable; unsigned int unknown; void *alias; void FUN_00ae91f0();
 ~ScrapListBase(){ vtable=&DAT_01094e5c; FUN_00ae91f0(); FUN_00aa10f0(alias); }
};
class ScrapListCleanup : public ScrapListBase { public: ~ScrapListCleanup() { FUN_00ae91f0();
unsigned int spare0;
unsigned int spare1;
unsigned int spare2;
unsigned int spare3;
}};
class ScrapListShell : public ScrapListCleanup { public: ~ScrapListShell(){ vtable=&DAT_01094e3c; } };
ScrapListShell DAT_011f3308;
