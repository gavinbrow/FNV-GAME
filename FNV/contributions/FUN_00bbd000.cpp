struct Stage { int unk00; int unk04; unsigned char active; };
extern Stage* DAT_01201090;
extern char DAT_010a1cac;
struct Frame {
    int m00;
    void* m04;
    int m08;
    int m0c;
    int m10;
    int m14;
    int m18;
    int m1c;
  unsigned short m20;
};
struct Parameters {
    int m00;
    int m04;
    int m08;
    int m0c;
    int m10;
    int m14;
    int m18;
    int m1c;
    int m20;
    int m24;
    int m28;

};
struct Pipeline {
 void FUN_00e6fe30(Parameters* params, int extra, int a, int b, int c);
};
extern Pipeline* DAT_011f9508;
struct Map {
  virtual void skipped0();
  virtual void skipped1();
  virtual void skipped2();
  virtual void skipped3();
  virtual void skipped4();
  virtual void skipped5();
  virtual void skipped6();
  virtual void skipped7();
  virtual void skipped8();
  virtual void skipped9();
  virtual void skipped10();
  virtual void skipped11();
  virtual void skipped12();
  virtual void skipped13();
  virtual void skipped14();
  virtual void skipped15();
  virtual void skipped16();
  virtual void skipped17();
  virtual void skipped18();
  virtual void skipped19();
  virtual void skipped20();
  virtual void skipped21();
  virtual void skipped22();
  virtual void skipped23();
  virtual void skipped24();
  virtual void skipped25();
  virtual void skipped26();
  virtual void skipped27();
  virtual void* GetResource(const void* key);

};
struct Device {
  virtual void skipped0();
  virtual void skipped1();
  virtual void skipped2();
  virtual void skipped3();
  virtual void skipped4();
  virtual void skipped5();
  virtual void skipped6();
  virtual void skipped7();
  virtual void skipped8();
  virtual void skipped9();
  virtual void skipped10();
  virtual void skipped11();
  virtual void skipped12();
  virtual void skipped13();
  virtual void skipped14();
  virtual void skipped15();
  virtual void skipped16();
  virtual void skipped17();
  virtual void skipped18();
  virtual void skipped19();
  virtual void skipped20();
  virtual void skipped21();
  virtual void skipped22();
  virtual void skipped23();
  virtual void skipped24();
  virtual void skipped25();
  virtual void skipped26();
  virtual void skipped27();
  virtual void skipped28();
  virtual void skipped29();
  virtual void Draw(void* r, int a, unsigned short b, int c, void* d);

};
struct DeviceOwner {
    int m00;
    int m04;
    int m08;
    int m0c;
    int m10;
    int m14;
    int m18;
    int m1c;
    int m20;
    int m24;
    int m28;
    int m2c;
    int m30;
    int m34;
    int m38;
    int m3c;
    int m40;
    int m44;
    int m48;
    int m4c;
    int m50;
    int m54;
    int m58;
  Device* m5c;
};
extern DeviceOwner* DAT_0126f74c;
typedef void (__thiscall *RenderDrawFn)(Device*, void*, int, unsigned short, int, void*);
struct FUN_00bbd000_cls {
    int m00;
    int m04;
    int m08;
    int m0c;
    int m10;
    int m14;
    int m18;
    int m1c;
    int m20;
    int m24;
    int m28;
    int m2c;
    int m30;
  Map* m34;
  int m38;
    int m3c;
    int m40;
    int m44;
    int m48;
    int m4c;
    int m50;
    int m54;
    int m58;
    int m5c;
    int m60;
    int m64;
    int m68;
    int m6c;
  Map* m70;
 int FUN_00bbd000(int a1, Parameters* params, Frame* frame, int a4, int a5, int a6, int extra, int a8);
};
int FUN_00bbd000_cls::FUN_00bbd000(int a1, Parameters* params, Frame* frame, int a4, int a5, int a6, int extra, int a8) {
 if (frame && m38 == 0 && ((DAT_01201090 && DAT_01201090->active) || m34 == m70)) {
  DAT_011f9508->FUN_00e6fe30(params, extra, 0, 3, 1);
  Map* resource = m70;
  int texture = params->m28;
  int address = params->m20;
  if (m34 == resource) {
   Device* device = DAT_0126f74c->m5c;
   RenderDrawFn* slot = (RenderDrawFn*)((char*)*(void**)device + 0x78);
   (*slot)(device, resource->GetResource(&DAT_010a1cac), texture, frame->m20, address, frame->m04);
  } else {
   Device* device = DAT_0126f74c->m5c;
   device->Draw(DAT_01201090, texture, frame->m20, address, frame->m04);
  }
 }
 return 0;
}