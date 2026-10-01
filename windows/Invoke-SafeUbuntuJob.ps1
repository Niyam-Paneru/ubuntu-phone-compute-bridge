[CmdletBinding()]
param(
    [ValidateSet('health','python-smoke','benchmark','setup')]
    [string]$Job = 'health',

    [Parameter(Mandatory)]
    [ipaddress]$HostAddress,

    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9_]+$')]
    [string]$User,

    [ValidateRange(1,65535)]
    [int]$Port = 8022,

    [Parameter(Mandatory)]
    [string]$IdentityFile
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($HostAddress.AddressFamily -ne [Net.Sockets.AddressFamily]::InterNetwork) {
    throw 'This public example accepts IPv4 only.'
}

if (-not (Test-Path -LiteralPath $IdentityFile -PathType Leaf)) {
    throw "SSH identity file not found: $IdentityFile"
}

$jobScripts = @{
    'health'       = 'printf ''{"job":"health","execution_location":"phone-ubuntu","ok":true}\n'''
    'python-smoke' = 'python3 -c ''import json; print(json.dumps({"job":"python-smoke","execution_location":"phone-ubuntu","ok":True,"value":2+2}))'''
    'benchmark'    = 'python3 -c ''import json,time; s=time.perf_counter(); sum(i*i for i in range(200000)); print(json.dumps({"job":"benchmark","execution_location":"phone-ubuntu","ok":True,"elapsed":time.perf_counter()-s}))'''
    'setup'        = 'python3 -c ''import json,shutil; print(json.dumps({"job":"setup","execution_location":"phone-ubuntu","ok":bool(shutil.which("python3"))}))'''
}

$remote = $jobScripts[$Job]
$sshArgs = @(
    '-p', [string]$Port,
    '-o', 'BatchMode=yes',
    '-o', 'StrictHostKeyChecking=yes',
    '-o', 'ConnectTimeout=5',
    '-o', 'ServerAliveInterval=10',
    '-o', 'ServerAliveCountMax=2',
    '-i', $IdentityFile,
    "$User@$($HostAddress.IPAddressToString)",
    $remote
)

$output = & ssh.exe @sshArgs
if ($LASTEXITCODE -ne 0) {
    throw "Remote job failed with SSH exit code $LASTEXITCODE"
}

$output
