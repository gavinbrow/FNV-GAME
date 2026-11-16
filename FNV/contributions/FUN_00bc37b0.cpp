struct Color4 { float r,g,b,a; };
struct RGBWords { unsigned int r,g,b; };
extern int DAT_010bab28;
extern RGBWords DAT_011a9be0;
extern float DAT_01016410;
struct FUN_00bc37b0_class { void FUN_00ba8e50(); void* FUN_00bc37b0(); };
void* FUN_00bc37b0_class::FUN_00bc37b0(){
 FUN_00ba8e50();
 *reinterpret_cast<int**>(this)=&DAT_010bab28;
 Color4& color=*reinterpret_cast<Color4*>(reinterpret_cast<char*>(this)+0x60);
 color.a=color.b=color.g=color.r=0.0f;
 RGBWords& rgb=*reinterpret_cast<RGBWords*>(&color);
 unsigned int red=DAT_011a9be0.r; double alpha=DAT_01016410; rgb.r=red; rgb.g=DAT_011a9be0.g; rgb.b=DAT_011a9be0.b; *reinterpret_cast<volatile float*>(&color.a)=alpha;
 *reinterpret_cast<int*>(reinterpret_cast<char*>(this)+0x1c)=0x16;
 return this;
}