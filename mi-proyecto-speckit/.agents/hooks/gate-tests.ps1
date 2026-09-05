# Hook de bloqueo: impide continuar si hay tests fallando.
python -m pytest --tb=no -q
if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("BLOQUEADO: hay tests fallando. Corrige antes de continuar.")
    exit 2
}
exit 0