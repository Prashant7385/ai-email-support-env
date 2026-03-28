from huggingface_hub import HfApi, login
import os

# Get token from environment variable (more secure)
HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = "Prashant7385/Openenvproject"

if not HF_TOKEN:
    print("❌ HF_TOKEN environment variable not set!")
    print("Set it with: $env:HF_TOKEN='your_token_here'")
    print("Or run: python -m huggingface_hub login")
    exit(1)

# Initialize API
api = HfApi()

try:
    # Try to create the repo (will fail if it already exists, which is fine)
    print(f"Creating/checking repository: {REPO_ID}...")
    api.create_repo(
        repo_id=REPO_ID,
        repo_type="space",
        space_sdk="docker",
        token=HF_TOKEN,
        exist_ok=True
    )
    print("✅ Repository ready!")
    
    # Upload the entire directory
    print(f"\nUploading files to https://huggingface.co/spaces/{REPO_ID}...")
    api.upload_folder(
        folder_path=".",
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="Initial commit: email environment structure",
        token=HF_TOKEN,
        ignore_patterns=["*.pyc", "__pycache__", "*.pth"]  # Skip compiled files
    )
    print("\n✅ Upload successful!")
    print(f"🎉 View your Space at: https://huggingface.co/spaces/{REPO_ID}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if your token is valid at: https://huggingface.co/settings/tokens")
    print("2. Make sure you have write access to Prashant7385 account")
    print("3. Try logging in with: python -m huggingface_hub login")
