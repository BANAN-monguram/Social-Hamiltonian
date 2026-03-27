$ErrorActionPreference = "Stop"

$src = "main.c"
$out = "simulation.exe"

Write-Host "Compiling $src..."
gcc -o $out $src

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful: $out"
    Write-Host "Running simulation..."
    Write-Host "--------------------"
    ./$out
} else {
    Write-Error "Build failed."
}
