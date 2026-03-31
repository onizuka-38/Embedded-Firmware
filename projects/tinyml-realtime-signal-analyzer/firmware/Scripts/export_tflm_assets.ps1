param(
    [Parameter(Mandatory=$true)][string]$TflitePath,
    [string]$DatasetDir = "projects/tinyml-realtime-signal-analyzer/ml/data/raw",
    [int]$WindowSize = 128,
    [int]$Stride = 32
)

python projects/tinyml-realtime-signal-analyzer/ml/export/export_model.py `
    --dataset-dir $DatasetDir `
    --window-size $WindowSize `
    --stride $Stride `
    --tflite-path $TflitePath
