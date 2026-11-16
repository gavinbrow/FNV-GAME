class FloatSource {public: float FUN_006a78f0();};
struct FloatGetterGlobal { float* FUN_00403e20(); };
extern FloatGetterGlobal DAT_011cfb5c, DAT_011cf264;
float FUN_006479e0(FloatSource* src) {
float result; if(src!=0) result=src->FUN_006a78f0(); else result=0.0f;
float factor=result;
factor = (*DAT_011cf264.FUN_00403e20() + (+*DAT_011cfb5c.FUN_00403e20())) * factor;
return factor;
}