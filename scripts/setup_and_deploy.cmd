@echo off
title Omniverse Multi-Modal Studio Setup System Engine
echo ================================================================
echo OMNIVERSE AI MULTIMEDIA ENGINE: CMD WORKSPACE AUTOMATOR
echo ================================================================

:: 1. Establish core target structural directories
echo [*] Generating deep workspace directories on host file-system...
mkdir .github\workflows 2>nul
mkdir backend\app\api 2>nul
mkdir backend\app\core 2>nul
mkdir backend\app\models 2>nul
mkdir backend\app\services 2>nul
mkdir frontend\public 2>nul
mkdir frontend\src\components 2>nul
mkdir frontend\src\hooks 2>nul
mkdir frontend\src\pages 2>nul

:: 2. Write empty initialization system configuration indicators
echo [*] Formatting structural system component code packages...
type null > backend\app\__init__.py 2>nul
type null > backend\app\api\__init__.py 2>nul
type null > backend\app\core\__init__.py 2>nul
type null > backend\app\models\__init__.py 2>nul
type null > backend\app\services\__init__.py 2>nul

:: 3. Test local environment orchestration links
echo [*] Querying system container parameters...
where docker >nul 2>nul
if %errorlevel% equ 0 (
    echo [+] Local engine detected. Provisioning local container workspace stacks...
    docker compose build
    echo [+] Local setup successfully compiled. Execute 'docker compose up' to open studio.
) else (
    echo [-] Local Docker Desktop is missing or inactive. Skipping container validation.
)

echo ================================================================
echo PRODUCTION CLOUD DISPATCH PROTOCOL GUIDE
echo ================================================================
echo RENDER (FREE BACKEND API): Deploy your repo as a 'Docker' Web Service.
echo VERCEL (FREE FRONTEND UI): Run 'npm install -g vercel' then execute 'vercel --prod' inside your /frontend directory.
echo ================================================================
pause
