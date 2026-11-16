struct EmptyTag {};
int __cdecl FUN_0065fe40(int*);
int __cdecl FUN_0065eac0(int,int,int,EmptyTag,EmptyTag,EmptyTag);
int __cdecl FUN_0065e7c0(int first,int last,int destination)
{
 int result=((last-first)/88)*88+destination;
 { EmptyTag firstZero = {}; EmptyTag secondZero = {}; EmptyTag option;
 FUN_0065eac0(first,last,FUN_0065fe40(&destination),option,secondZero,firstZero);
 }
 return result;
}