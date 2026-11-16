extern const double DAT_01011588; extern const double DAT_01021928; extern const double DAT_010ea600; extern const double DAT_010737c8; extern const float DAT_010ea608;
struct FnParams { int first,last; float lower,upper,default_scale; int unknown14,unknown18,unknown1c,unknown20,unknown24,unknown28,unknown2c,unknown30,unknown34; float displacement; };
struct FnvCurve { int unknown00,unknown04,unknown08,unknown0c,unknown10; float coefficient; int unknown18; float threshold; float FUN_00e0a850(FnParams* p); };
float FnvCurve::FUN_00e0a850(FnParams* p) {
 float phase=p->displacement-(float)((p->upper+p->lower)*DAT_01011588);
 float scale;
 if(p->first<p->last) {
  float width=p->upper-p->lower;
  float bound=threshold;
  float selected;
  if(bound<width) selected=bound; else selected=width;
  if(width+selected>0.0f) scale=1.0f/(width+selected);
  else scale=DAT_010ea608;
 } else scale=p->default_scale;
 float x=scale*phase;
 if(x>0.0f) return 0.0f;
 float x2=x*x;
 float x4=x2*x2;
 float x8=x4*x4;
float poly=(x2*DAT_010ea600+x4*DAT_01021928)+x8*DAT_010737c8;
return poly*coefficient;}