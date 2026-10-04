#!/bin/bash
echo "=== 1. EJECUTANDO PRUEBAS UNITARIAS (PyTest) ==="
pytest -v test_saocom.py

echo ""
echo "=== 2. EJECUTANDO PRUEBA DE API (Bruno CLI) ==="
bru run consulta_admin.bru

echo ""
echo "=== PIPELINE DE AUDITORÍA COMPLETADO ==="
