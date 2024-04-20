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

    $countryMapping = @{}
    $locations | ForEach-Object {
        $countryMapping[$_.Shorthand.ToLower()] = $_.Country
        $countryMapping[$_.Country.ToLower()] = $_.Country
    }

    if ($ListLocations) {
        Write-Host "Available locations:"
        $locations | ForEach-Object {
            Write-Host "$($_.Country) ($($_.Shorthand))"
        }
        return
    }

    if ($Country) {
        $normalizedCountry = $Country.ToLower()

        if ($countryMapping.ContainsKey($normalizedCountry)) {
            $fullCountry = $countryMapping[$normalizedCountry]
            $shorthandCountry = ($locations | Where-Object { $_.Country -eq $fullCountry }).Shorthand
        }
        else {
            Write-Host "Invalid country provided."
            return
        }

        if ($locations | Where-Object { $_.Shorthand -eq $shorthandCountry }) {
            Write-Host "Setting Mullvad location to $fullCountry"
            mullvad relay set location $shorthandCountry
        }
        else {
            Write-Host "Invalid country shorthand provided."
            return
        }
    }
    else {
        $randomIndex = Get-Random -Minimum 0 -Maximum $locations.Count
        Write-Host "Setting Mullvad location to $($locations[$randomIndex].Country)"
        mullvad relay set location $($locations[$randomIndex].Shorthand.ToLower())
    }

    Start-Sleep -Seconds 2

    mullvad status
}
