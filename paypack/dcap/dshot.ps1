[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

function Get-ScreenCapture {

    param(
        [switch]$OfWindow
    )

    begin {
        Add-Type -AssemblyName System.Drawing
        $jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.FormatDescription -eq "JPEG" }
    }
    process {
        Start-Sleep -Milliseconds 250
        if ($OfWindow) {
            [System.Windows.Forms.Sendkeys]::SendWait("%{PrtSc}")
        } else {
            [System.Windows.Forms.Sendkeys]::SendWait("{PrtSc}")
        }
        Start-Sleep -Milliseconds 250
        $bitmap = [System.Windows.Forms.Clipboard]::GetImage()
        $ep = New-Object System.Drawing.Imaging.EncoderParameters
        $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]100)
        $ScreenCapturePathBase = "$pwd\screen_capture"
        $c = 0
        while (Test-Path "${ScreenCapturePathBase}${c}.jpg") {
            $c++
        }
        $bitmap.Save("${ScreenCapturePathBase}${c}.jpg", $jpegCodec, $ep)
    }
  
}

Get-ScreenCapture -OfWindow
