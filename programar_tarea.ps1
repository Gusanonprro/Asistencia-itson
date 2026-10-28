# Crea (o actualiza) la tarea programada que registra la asistencia.
# Cambia los días y la hora de tu clase aquí:
$Dias = "Monday", "Wednesday", "Friday"
$Hora = "10:00"

$bat = Join-Path $PSScriptRoot "ejecutar_asistencia.bat"
$accion = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"`"$bat`"`""
$disparador = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Dias -At $Hora
$config = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours 1)

Register-ScheduledTask -TaskName "Asistencia ITSON" -Action $accion -Trigger $disparador `
    -Settings $config -Description "Registra asistencia en ivirtual ITSON" -Force | Out-Null

$siguiente = (Get-ScheduledTaskInfo -TaskName "Asistencia ITSON").NextRunTime
Write-Host "Tarea 'Asistencia ITSON' lista. Próxima ejecución: $siguiente"
