struct AudioInterface {
 virtual void Reserved0();
 virtual void Reserved1();
 virtual void Reserved2();
 virtual void Reserved3();
 virtual void Reserved4();
 virtual void Reserved5();
 virtual void Reserved6();
 virtual void Reserved7();
 virtual void Reserved8();
 virtual void Reserved9();
 virtual void Reserved10();
 virtual void Reserved11();
 virtual void Reserved12();
 virtual void Apply(void*, float);
};
struct AudioHandle { AudioInterface* system; void* object; void FUN_00dbad20(float); };
void AudioHandle::FUN_00dbad20(float value) { system->Apply(object, value); }
