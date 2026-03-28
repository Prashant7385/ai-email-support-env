@echo off
echo ========================================
echo 🚀 UPLOADING TO GITHUB
echo ========================================
echo.

echo Step 1: Initializing git repository...
git init
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Creating commit...
git commit -m "Initial commit: Complete OpenEnv email environment with inference.py"
echo.

echo Step 4: Setting up remote repository...
git remote add origin https://github.com/Prashant7385/ai-email-support-env.git
echo.

echo Step 5: Renaming branch to main...
git branch -M main
echo.

echo Step 6: Pushing to GitHub...
echo IMPORTANT: You will be prompted for GitHub credentials.
echo Use your GitHub username and password (or personal access token).
echo.
git push -u origin main

echo.
echo ========================================
if %errorlevel% equ 0 (
    echo ✅ SUCCESS! Files uploaded to GitHub!
    echo 🔗 View at: https://github.com/Prashant7385/ai-email-support-env
) else (
    echo ⚠️ Upload may have encountered issues.
    echo Check the error messages above.
)
echo ========================================
pause
