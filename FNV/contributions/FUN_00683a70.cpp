struct Point {float x,y,z;};
struct Decal {bool FUN_00683a70(int,int,bool,const unsigned short*,const Point*,const unsigned short*);};
bool Decal::FUN_00683a70(int triangle,int base,bool strip,const unsigned short* indices,const Point* vertices,const unsigned short* remap)
{
 int flags;
 { bool result=false;flags=0;
  for(int i=0;i<3;++i) {
   int inside;
   {unsigned short vertex=0;inside=0;
    if(strip)vertex=indices[triangle+i]+base;
    else vertex=indices[triangle*3+i]+base;
    if(remap)vertex=remap[vertex];
    if(vertices[vertex].x<0.0)flags|=1;
    else if(vertices[vertex].x>1.0)flags|=2;
    else ++inside;
    if(vertices[vertex].y<0.0)flags|=4;
    else if(vertices[vertex].y>1.0)flags|=8;
    else ++inside;
    if(vertices[vertex].z>0.10000000149011612){flags|=16;++inside;}
    if(inside==3)return true;
   }
  }
  if(((flags&3)==3 || (flags&12)==12) && (flags&16))result=true;
  return result;
 }
}
