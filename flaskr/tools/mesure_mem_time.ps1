# Measure command execution time and memory usage
#.\mesure_mem_time.ps1 -cmd "cmd to run" -cmd2 "cmd2 to run"

# for linux
# /usr/bin/time -v "command to run"
# from the output
# User time (seconds): 0.33
# Maximum resident set size (kbytes): 3192

param ( [string]$cmd, [string]$cmd2 )
$process = Start-Process $cmd -PassThru
Start-Sleep -Milliseconds 100
$memoryUsage = (Get-Process -Id $process.Id).WorkingSet64 / (1024 * 1024)
$process.WaitForExit()
$cpuTime = $process.TotalProcessorTime.TotalMilliseconds / 1000
# $memoryUsage = $process.PrivateMemorySize64 / (1024 * 1024)

Write-Output "CPU Time: $cpuTime sec"
Write-Output "Memory Usage: $memoryUsage Mb"
