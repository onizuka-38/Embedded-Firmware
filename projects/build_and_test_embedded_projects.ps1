$ErrorActionPreference = "Stop"

$clang = "C:\Users\parkdonghyeon\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260421-ucrt-x86_64\bin\clang.exe"
if (-not (Test-Path $clang)) {
    throw "clang not found: $clang"
}

$root = $PSScriptRoot
$outRoot = Join-Path $root "build-host-tests"
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

function Build-And-Run([string]$name, [string[]]$sources, [string[]]$includes) {
    $exe = Join-Path $outRoot ("$name.exe")

    $args = @("-std=c11", "-Wall", "-Wextra", "-Werror")
    foreach ($inc in $includes) { $args += @("-I", $inc) }
    $args += $sources
    $args += @("-o", $exe)

    & $clang @args
    if ($LASTEXITCODE -ne 0) { throw "compile failed: $name" }

    & $exe
    if ($LASTEXITCODE -ne 0) { throw "test failed: $name" }
}

Build-And-Run "ble_sensor_hub" @(
    (Join-Path $root "stm32-ble-sensor-hub/firmware/Core/Src/sensor_hub.c"),
    (Join-Path $root "stm32-ble-sensor-hub/firmware/Core/Src/ble_link.c"),
    (Join-Path $root "stm32-ble-sensor-hub/firmware/Tests/test_ble_sensor_hub.c")
) @(
    (Join-Path $root "stm32-ble-sensor-hub/firmware/Core/Inc")
)

Build-And-Run "motor_control" @(
    (Join-Path $root "freertos-motor-control/firmware/Core/Src/pid.c"),
    (Join-Path $root "freertos-motor-control/firmware/Core/Src/motor_control.c"),
    (Join-Path $root "freertos-motor-control/firmware/Tests/test_motor_control.c")
) @(
    (Join-Path $root "freertos-motor-control/firmware/Core/Inc")
)

Build-And-Run "bms_monitor" @(
    (Join-Path $root "can-bms-monitor/firmware/Core/Src/bms_state.c"),
    (Join-Path $root "can-bms-monitor/firmware/Tests/test_bms_state.c")
) @(
    (Join-Path $root "can-bms-monitor/firmware/Core/Inc")
)

Write-Host "All embedded host tests passed." -ForegroundColor Green
