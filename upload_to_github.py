"""
GitHub Upload Script for Email Environment Project

This script uploads the project to GitHub using the huggingface_hub library approach,
but adapted for GitHub via git commands or direct API.

Note: For GitHub, we need to use git commands since there's no direct equivalent
to huggingface_hub.upload_folder() for GitHub.

Alternative: This script will prepare files and provide instructions for manual upload.
"""

import os
import subprocess
import sys

def check_git_installed():
    """Check if git is installed and available"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        return True, result.stdout.strip()
    except FileNotFoundError:
        return False, "Git is not installed or not in PATH"

def upload_to_github():
    """Upload project to GitHub repository"""
    
    print("="*60)
    print("🚀 UPLOADING TO GITHUB")
    print("="*60)
    
    # Check git installation
    git_installed, git_info = check_git_installed()
    
    if not git_installed:
        print("\n❌ Git is not installed!")
        print("\nPlease install Git from: https://git-scm.com/download/win")
        print("\nAlternatively, you can:")
        print("1. Go to: https://github.com/Prashant7385/ai-email-support-env")
        print("2. Click 'Add file' → 'Upload files'")
        print("3. Drag and drop all project files")
        return False
    
    print(f"\n✅ {git_info}")
    
    # Repository URL
    repo_url = "https://github.com/Prashant7385/ai-email-support-env.git"
    
    print(f"\n📦 Target Repository: {repo_url}")
    
    # Create .gitignore
    print("\n📝 Creating .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
*.log

# Compiled
*.pyc
*.pyo
*.pyd
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore")
    
    print("\n" + "="*60)
    print("MANUAL GIT COMMANDS (Run these in terminal):")
    print("="*60)
    print("""
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Complete email environment with OpenEnv spec"

# Add remote repository
git remote add origin https://github.com/Prashant7385/ai-email-support-env.git

# Push to GitHub
git branch -M main
git push -u origin main
""")
    
    print("\n" + "="*60)
    print("OR Upload via GitHub Web Interface:")
    print("="*60)
    print("""
1. Go to: https://github.com/Prashant7385/ai-email-support-env

2. Click "uploading an existing file" link

3. Drag and drop these files:
   ✓ Dockerfile
   ✓ README.md  
   ✓ REQUIREMENTS_CHECKLIST.md
   ✓ baseline_inference.py
   ✓ client.py
   ✓ models.py
   ✓ openenv.yaml
   ✓ upload_to_hf.py
   ✓ server/app.py
   ✓ server/environment.py
   ✓ server/grader.py
   ✓ server/__init__.py

4. Click "Commit changes"
""")
    
    return True


if __name__ == "__main__":
    upload_to_github()
