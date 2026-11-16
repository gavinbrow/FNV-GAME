exec(open("setup.py").read())
s=set(orel_data[dcode].tolist()); a=np.array(sorted(s))
runs=[];i=0
while i<len(a):
    j=i
    while j+1<len(a) and a[j+1]-a[j]==4: j+=1
    runs.append(j-i+1); i=j+1
r=np.array(runs); print('data->code runs',len(r),'fields in runs>=2',int(r[r>=2].sum()),'runs>=2',int((r>=2).sum()),'singletons',int((r==1).sum()))
# singletons at stride 8 w/ other pointer (unwind map: int,ptr) can't tell; done
