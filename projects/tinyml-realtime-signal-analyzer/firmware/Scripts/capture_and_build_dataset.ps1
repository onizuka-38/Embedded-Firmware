param(
    [string]$Port = "",
    [int]$Baud = 115200,
    [int]$SecondsPerClass = 60,
    [string]$OutDir = "projects/tinyml-realtime-signal-analyzer/ml/data/raw/sessions"
)

if ([string]::IsNullOrWhiteSpace($Port)) {
    $candidate = Get-CimInstance Win32_SerialPort |
        Where-Object { $_.DeviceID -match '^COM[0-9]+$' } |
        Select-Object -First 1

    if ($null -eq $candidate) {
        throw "No COM port detected. Pass -Port COMx explicitly."
    }

    $Port = $candidate.DeviceID
}

$normal = Join-Path $OutDir "normal.csv"
$anomaly = Join-Path $OutDir "anomaly.csv"
$merged = "projects/tinyml-realtime-signal-analyzer/ml/data/raw/capture_merged.csv"

python projects/tinyml-realtime-signal-analyzer/ml/data_capture/capture_uart_csv.py `
    --port $Port --baud $Baud --seconds $SecondsPerClass --output $normal --label 0

python projects/tinyml-realtime-signal-analyzer/ml/data_capture/capture_uart_csv.py `
    --port $Port --baud $Baud --seconds $SecondsPerClass --output $anomaly --label 1

python projects/tinyml-realtime-signal-analyzer/ml/data_capture/merge_captures.py `
    --input-dir $OutDir --output $merged --min-rows 200
