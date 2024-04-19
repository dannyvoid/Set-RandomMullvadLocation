function Set-RandomMullvadLocation {
    [CmdletBinding()]
    param (
        [string]$Country,
        [switch]$ListLocations
    )

    $output = mullvad relay list
    $locations = $output -split "`n" | ForEach-Object {
        if ($_ -match '^([A-Za-z\s]+) \(([a-z]+)\)$') {
            @{
                Shorthand = $matches[2]
                Country   = $matches[1].Trim()
            }
        }
    } | Where-Object { $_ -ne $null }

    if ($ListLocations) {
        Write-Host "Available locations:"
        $locations | ForEach-Object {
            Write-Host "$($_.Country) ($($_.Shorthand))"
        }
        return
    }

    if ($Country) {
        if ($locations | Where-Object { $_.Shorthand -eq $Country.ToLower() }) {
            mullvad relay set location $Country
        }
        else {
            Write-Host "Invalid country shorthand provided."
            return
        }
    }
    else {
        $randomIndex = Get-Random -Minimum 0 -Maximum $locations.Count
        mullvad relay set location $($locations[$randomIndex].Shorthand)
    }

    Start-Sleep -Seconds 2

    mullvad status -v
}
