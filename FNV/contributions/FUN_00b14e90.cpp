#include <stdlib.h>
float FUN_00b14e90(float minimum,float maximum) {
 float fraction=(float)(rand()/32767.0);
 float range=maximum-minimum;
 return fraction*range+minimum;
}
