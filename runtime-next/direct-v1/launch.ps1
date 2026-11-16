param([string]$Exe='FalloutNV_direct.exe',[int[]]$Times=@(10,30,60),[string]$Tag='t1')
Add-Type -AssemblyName System.Drawing,System.Windows.Forms
Add-Type @"
using System;using System.Runtime.InteropServices;
public class W{[DllImport("user32.dll")]public static extern bool IsHungAppWindow(IntPtr h);
[DllImport("user32.dll")]public static extern bool GetWindowRect(IntPtr h,out RECT r);
[DllImport("user32.dll")]public static extern bool PrintWindow(IntPtr h,IntPtr dc,uint f);
public struct RECT{public int L,T,R,B;}}
"@
$root='C:\Projects\Decompilation\runtime-next\direct-v1'
$p=Start-Process -FilePath "$root\run\$Exe" -WorkingDirectory "$root\run" -PassThru
$t0=Get-Date
foreach($t in $Times){
  $left=$t-((Get-Date)-$t0).TotalSeconds; if($left -gt 0){Start-Sleep -Seconds ([int]$left)}
  $p.Refresh()
  if($p.HasExited){ "t=$t EXITED code=0x{0:X}" -f $p.ExitCode; break }
  $p.Refresh()
  "t=$t alive title='$($p.MainWindowTitle)' hung=$([W]::IsHungAppWindow($p.MainWindowHandle)) ws=$([int]($p.WorkingSet64/1MB))MB cpu=$($p.CPU)"
  if($p.MainWindowHandle -ne 0){
    $r=New-Object W+RECT; [void][W]::GetWindowRect($p.MainWindowHandle,[ref]$r)
    $w=$r.R-$r.L;$h=$r.B-$r.T
    if($w -gt 0 -and $h -gt 0){$bmp=New-Object Drawing.Bitmap $w,$h;$g=[Drawing.Graphics]::FromImage($bmp);$g.CopyFromScreen($r.L,$r.T,0,0,$bmp.Size);$bmp.Save("$root\shot_${Tag}_$t.png");$g.Dispose();$bmp.Dispose()}
  }
}
if(-not $p.HasExited){ "still running pid $($p.Id)" }
