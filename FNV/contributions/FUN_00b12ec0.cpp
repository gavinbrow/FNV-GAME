extern "C" double __cdecl sin(double); extern "C" double __cdecl cos(double); extern double DAT_010a4d90;
struct RotationMatrix { float m00,m01,m02,m10,m11,m12,m20,m21,m22; void __thiscall FUN_00b12ec0(float angle,float x,float y,float z); };
void RotationMatrix::FUN_00b12ec0(float angle,float x,float y,float z) {
 float cosA=(float)((float)(sin((float)(angle/DAT_010a4d90))));
 float sinA=(float)((float)(cos((float)(angle/DAT_010a4d90))));
 float zAxis=1.0f-sinA;
 float xAxis=x,yAxis=y,oneMinusCosA=z;
 m00=zAxis*xAxis*xAxis+sinA;
 m01=zAxis*xAxis*yAxis+cosA*oneMinusCosA;
 m02=zAxis*xAxis*oneMinusCosA-cosA*yAxis;
 m10=zAxis*xAxis*yAxis-cosA*oneMinusCosA;
 m11=zAxis*yAxis*yAxis+sinA;
 m12=zAxis*yAxis*oneMinusCosA+cosA*xAxis;
 m20=zAxis*xAxis*oneMinusCosA+cosA*yAxis;
 m21=zAxis*yAxis*oneMinusCosA-cosA*xAxis;
 m22=zAxis*oneMinusCosA*oneMinusCosA+sinA;
}