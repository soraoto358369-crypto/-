@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "LOG=%~dp0診断結果.txt"

echo ============================================================
echo   note-article-system 診断
echo   15秒ほどかかります。そのままお待ちください...
echo ============================================================

call :diag > "%LOG%" 2>&1

rem テスト起動したサーバーを終了しておく
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8788 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }" >nul 2>&1
del /q "%~dp0_server_test.log" >nul 2>&1

echo.
echo 診断が終わりました。「診断結果.txt」を開きます。
echo この内容をそのままコピーして貼り付けてください。
start "" notepad "%LOG%"
pause
exit /b

:diag
echo ============================================
echo   note-article-system 診断結果
echo   %DATE% %TIME%
echo ============================================
echo.

echo [1] 実行フォルダ
echo %CD%
echo.

echo [2] Python
where python
python --version
echo   -- py ランチャー --
where py
py -3 --version
echo.

echo [3] Node.js / npm
where node
node -v
where npm
echo.

echo [4] claude CLI
where claude
echo.

echo [5] Flask
python -c "import flask, sys; print('flask OK', flask.__version__)"
echo.

echo [6] 必要ファイルの有無
if exist "webapp\server.py" (echo   webapp\server.py ... OK) else (echo   webapp\server.py ... 見つかりません)
if exist "webapp\static\index.html" (echo   webapp\static\index.html ... OK) else (echo   webapp\static\index.html ... 見つかりません)
if exist "CLAUDE.md" (echo   CLAUDE.md ... OK) else (echo   CLAUDE.md ... 見つかりません)
if exist "config.json" (echo   config.json ... OK) else (echo   config.json ... 見つかりません)
echo.

echo [7] ポート8788の使用状況（起動前）
netstat -ano | findstr :8788
echo   ^(何も出なければ未使用＝正常^)
echo.

echo [8] サーバー起動テスト
start /b "" cmd /c "python webapp\server.py > _server_test.log 2>&1"
powershell -NoProfile -Command "Start-Sleep -Seconds 8"
powershell -NoProfile -Command "try{ $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',8788); $c.Close(); Write-Output '  ==> 接続OK: サーバーは正常に起動しました' }catch{ Write-Output '  ==> 接続NG: サーバーが起動できていません' }"
echo.

echo [9] サーバーの出力（ここにエラーが出ます）
if exist "_server_test.log" (type "_server_test.log") else (echo   ログが作成されませんでした = python が起動していません)
echo.

echo ============================================
echo   診断ここまで
echo ============================================
exit /b
