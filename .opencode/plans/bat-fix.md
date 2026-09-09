# Fix run.bat — Input Redirection Error

## Problem
When running `run.bat` with piped input (or from some shells), commands like
`docker compose`, `curl`, and `Timeout` consume leftover stdin, producing:
```
ERROR: Input redirection is not supported, exiting the process immediately.
```

## Root Cause
Every `docker compose` and `curl` command reads stdin. When stdin is redirected
(piped input, PowerShell redirect), these commands try to parse the piped data
as their own input and fail.

## Fix
Add `< nul` after every command that shouldn't read stdin. This redirects stdin
from the null device, preventing unwanted input consumption.

## Changes to `run.bat`

| Line | Current | Fixed |
|------|---------|-------|
| 54   | `docker compose up -d` | `docker compose up -d < nul` |
| 68   | `curl -s -o nul "%URL%/health" >nul 2>&1` | `curl -s -o nul "%URL%/health" < nul 2>&1` |
| 95   | `docker compose up --build -d` | `docker compose up --build -d < nul` |
| 109  | `curl -s -o nul "%URL%/health" >nul 2>&1` | `curl -s -o nul "%URL%/health" < nul 2>&1` |
| 117  | `docker compose down` | `docker compose down < nul` |
| 125  | `docker compose restart` | `docker compose restart < nul` |
| 132  | `docker compose logs -f` | `docker compose logs -f < nul` |

## Why `< nul` (not `< CON:`)
- `nul` is Windows's null device — always available, no interaction needed
- `CON:` is the console — could still block waiting for input
- `< nul` is the standard pattern for this problem in .bat files

## Verification
After fix, run:
```powershell
# Test menu parses (choose 6 = exit)
"6`r`n`r`n" | cmd /c run.bat

# Test option 1 start (no errors expected)
"1`r`n`r`n" | cmd /c run.bat
```
Both should complete with no "Input redirection" errors.
