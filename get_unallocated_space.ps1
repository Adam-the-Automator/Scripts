$Disks      = Get-CIMInstance -ClassName 'Win32_DiskDrive'
$Partitions = Get-CIMInstance -ClassName 'Win32_DiskPartition'

$Disks | ForEach-Object {
  [PSCustomObject]@{
    "Disk Index"            = $PSItem.Index
    "Partition Count"       = ($Partitions | Where-Object DiskIndex -EQ $PSItem.Index) | Measure-Object | Select-Object -ExpandProperty Count
    "Total Space(MB)"       = $PSItem.Size / 1MB
    "Unallocated Space(MB)" = ($PSItem.Size - ($Partitions | Where-Object DiskIndex -EQ $PSItem.Index | Measure-Object -Property Size -Sum).Sum) / 1MB
  }
}
