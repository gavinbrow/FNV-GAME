#include <math.h>
struct TextureCodec { unsigned int unk00,unk04,unk08,offset0c,converterIndex; unsigned char bytesPerElement; };
struct TexelSampler { unsigned int unk00,unk04,unk08,unk0c,unk10,unk14; TextureCodec* codec;
float FUN_00a3e5f0(unsigned int x,unsigned int y,float value); };
typedef void (__cdecl *ConverterFn)(float,unsigned int,unsigned int,float*);
extern ConverterFn DAT_011f3c18[];
float TexelSampler::FUN_00a3e5f0(unsigned int x,unsigned int y,float value) {
  unsigned int rgb=0, type;
  TextureCodec* squaredLength=codec;
  unsigned char base;
  if(squaredLength) {type=squaredLength->converterIndex;base=squaredLength->bytesPerElement;rgb=squaredLength->offset0c;}
  else {type=0;base=0;}
  float format[3];
  DAT_011f3c18[type](value,base*x+rgb,base*y+rgb,format);
  float stride=format[0]*format[0]+format[1]*format[1]+format[2]*format[2];
  return sqrtf(stride);
}
