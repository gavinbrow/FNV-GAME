struct Rec12Copy{unsigned int x,y,z;};struct CopyTagE{char v;};
Rec12Copy* __cdecl FUN_00ac1a50(Rec12Copy* first,Rec12Copy* last,Rec12Copy* dest){
CopyTagE tagC={};CopyTagE tagA;CopyTagE tagB=tagA;
{{CopyTagE tagH=tagC;}Rec12Copy* firstCopy=dest;Rec12Copy* result=first;
Rec12Copy* cur=(Rec12Copy*)((char*)firstCopy-((char*)last-(char*)result)/12*12);
CopyTagE tagF={};CopyTagE tagE={};CopyTagE c=tagF;CopyTagE tagD=tagE;
Rec12Copy* d=firstCopy;Rec12Copy* destArg=last;
while(result!=destArg){--destArg;--d;*d=*destArg;}return cur;}}