struct FnvFinitePair {float minimum; float maximum;};
struct FnvBounds {float minimum[4];float maximum[4];char* FUN_00da0b30(char* valid);};
char* FnvBounds::FUN_00da0b30(char* valid) {
FnvFinitePair pair;
for (int axis=0;axis<3;++axis) {
pair.minimum=minimum[axis];
if ((*(unsigned int*)&pair.minimum & 0x7f800000)==0x7f800000) goto invalid;
pair.maximum=maximum[axis];
if ((*(unsigned int*)&pair.maximum & 0x7f800000)==0x7f800000 || minimum[axis]>maximum[axis]) goto invalid;
}
*valid = 1; return valid;
invalid:
*valid = 0; return valid;
}