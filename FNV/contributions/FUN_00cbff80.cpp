#include <math.h>
extern double DAT_010c9300; extern double DAT_010c92f8;
extern double DAT_010c92f0; extern double DAT_01030f38; extern double DAT_0101ff40;
float __cdecl FUN_00cbff80(float x, float y) {
float ax=(float)fabs(x); float ay=(float)fabs(y);float t,result;
if(ax<=ay){t=ax/(float)(ay+DAT_010c9300);float tCopy = t;float partial=tCopy - (t * DAT_010c92f8) * t;result=partial-t*(t*(t*DAT_010c92f0));}
else {t=ay/(float)(ax+DAT_010c9300);float tCopy = t;float partial=tCopy - (t * DAT_010c92f8) * t;result=partial-t*(t*(t*DAT_010c92f0));result=(float)(DAT_01030f38-result);}
if(y<0.0f)result=(float)(DAT_0101ff40-result);
if(x<0.0f)result=-result;
return result;
}