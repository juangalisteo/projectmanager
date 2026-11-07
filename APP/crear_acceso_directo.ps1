# Crea un acceso directo a Project Manager en el escritorio, con su icono.
# Si queda el acceso directo antiguo (PROJECTMANAGER), lo quita.
$root = Split-Path -Parent $PSScriptRoot
$target = Join-Path $root "01_CREAR_PROYECTO.cmd"
$icon = Join-Path $PSScriptRoot "projectmanager.ico"
$desktop = [Environment]::GetFolderPath("Desktop")
$old = Join-Path $desktop "PROJECTMANAGER.lnk"
if (Test-Path $old) { Remove-Item $old }
$link = Join-Path $desktop "Project Manager.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($link)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $root
$shortcut.IconLocation = "$icon,0"
$shortcut.WindowStyle = 7
$shortcut.Description = "Crear un proyecto nuevo"
$shortcut.Save()
Write-Host "Acceso directo creado en el escritorio: $link"
