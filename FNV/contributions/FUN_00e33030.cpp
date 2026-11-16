typedef void (__cdecl *SplineDecodeFn)(int, void*);
extern int DAT_010eb3b8[]; extern int DAT_010eb3d0[]; extern SplineDecodeFn DAT_011be4b8[];
void __cdecl FUN_00e33030(int* cursor,int type,int lastFrame,int firstFrame,int endFrame,void* output) {
 int alignment=DAT_010eb3b8[type]; *cursor=(*cursor+alignment-1)&~(alignment-1);
 int stride=DAT_010eb3d0[type]; if(firstFrame>=0) {
 int byteOffset=(endFrame-firstFrame)*stride; SplineDecodeFn* volatile decodeSlot = &DAT_011be4b8[type];
 int remaining=firstFrame+1; char* destination=static_cast<char*>(output);
 do { (*decodeSlot)(*cursor+byteOffset,destination); byteOffset+=stride; destination+=16; }while(--remaining!=0);
 } *cursor+=(lastFrame+1)*stride;
}