Import-Module GroupPolicy
$Date = Get-Date -Format dd_MM_yyyy
$BackupDir = "c:\GPOBackup\$Date"
## Creates a directory to store the GPO reports
if (-Not(Test-Path -Path $BackupDir))  {
  New-Item -ItemType Directory $BackupDir -Force
}

# Get all GPOs with the gpo report type as XML and also look for the section <LinksTo> in the xml report.
# Consider only the GPOs that doesnt have <LinksTo> section.
Get-GPO -All | Where-Object { $_ | Get-GPOReport -ReportType XML | Select-String -NotMatch "<LinksTo>" } | ForEach-Object {
  # Backup the GPO, HTML report and saving the GPO details to text file are optional.
  Backup-GPO -Name $_.DisplayName -Path $BackupDir
   # Run the report and save as an HTML report to disk
  Get-GPOReport -Name $_.DisplayName -ReportType Html -Path "$BackupDir\$($_.DisplayName).html"
  # Create and append to a text file called UnlinkedGPOs.txt in the backup folder that
  # contains each GPO object that Get-GPO returns
  $_ | Select-Object * | Out-File "$BackupDir\UnLinkedGPOs.txt" -Append
  # Remove the GPO but first prompt before removing
  $_.Displayname | Remove-GPO -Confirm
}
