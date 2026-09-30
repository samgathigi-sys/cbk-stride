$ppt = $null
try {
    $ppt = [Runtime.InteropServices.Marshal]::GetActiveObject("PowerPoint.Application")
    Write-Host "PowerPoint Application Found."
    foreach ($pres in $ppt.Presentations) {
        Write-Host "Open Presentation: " $pres.FullName
        $pres.Close()
        Write-Host "Closed presentation."
    }
} catch {
    Write-Host "No active PowerPoint application or error:" $_.Exception.Message
}
