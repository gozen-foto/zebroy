$num = 0
while ($true){
    ./camcap.exe
    Move-Item -Path WCC.bmp -Destination "WCC${num}.bmp"
    while (Test-Path "WCC${num}.bmp") {
        $num++
    }
    Start-Sleep -Seconds 60
}