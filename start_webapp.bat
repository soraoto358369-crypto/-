@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   note-article-system  Web UI  (default: FULL-AUTO)
echo   フルオート: 確認なしで記事生成〜下書き投稿まで実行します
echo   ブラウザで開く: http://127.0.0.1:8788
echo ============================================================

rem Python を探す（python が無い環境では py -3 を使う）
set "PY="
python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
if not defined PY (
  py -3 --version >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo [ERROR] Python が見つかりません。
  echo         https://www.python.org/downloads/ からインストールし、
  echo         インストール時に "Add python.exe to PATH" にチェックを入れてください。
  pause
  exit /b 1
)
echo [INFO] Python: %PY%

rem 古いサーバーがポート8788を掴んでいたら自動で終了（再起動の罠を防ぐ）
echo [INFO] 既存サーバーを確認・終了します...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8788 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"

rem flask が無ければ自動インストール
%PY% -c "import flask" 2>nul
if errorlevel 1 (
  echo [INFO] Flask をインストールします...
  %PY% -m pip install flask
)

set NAS_ALLOW_FULL=1

rem サーバーが待受を開始してからブラウザを開く。
rem （先にブラウザを開くと、まだ起動途中のため「接続が拒否されました」になる）
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 120;$i++){ try{ $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',8788); $c.Close(); Start-Process 'http://127.0.0.1:8788'; break }catch{ Start-Sleep -Milliseconds 500 } }"

echo [INFO] サーバーを起動します。準備ができ次第ブラウザが自動で開きます...
echo [INFO] 開かない場合は http://127.0.0.1:8788 を手動で開いてください。
echo.
%PY% webapp\server.py
echo.
echo [INFO] サーバーが終了しました。このウィンドウは閉じて構いません。
pause
