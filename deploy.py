#!/usr/bin/env python3
"""
DataFixer Auto-Deploy Script
Helps deploy your DataFixer application to various platforms
"""

import os
import sys
import subprocess
import json

def run_command(command, shell=True):
    """Run a command and return output"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_requirements():
    """Check if basic requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if git is installed
    success, _, _ = run_command("git --version")
    if not success:
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Check if we're in a git repo
    if not os.path.exists('.git'):
        print("❌ Not a git repository. Initializing...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
    
    print("✅ Requirements check passed!")
    return True

def deploy_to_railway():
    """Deploy to Railway using CLI"""
    print("🚄 Deploying to Railway...")
    
    # Check if railway CLI is installed
    success, _, _ = run_command("railway --version")
    if not success:
        print("📦 Installing Railway CLI...")
        if sys.platform == "win32":
            print("Please install Railway CLI manually from: https://railway.app/cli")
            return False
        else:
            run_command("curl -fsSL https://railway.app/install.sh | sh")
    
    # Login and deploy
    print("🔐 Please login to Railway (browser will open)")
    run_command("railway login")
    
    print("🚀 Creating Railway project...")
    success, output, error = run_command("railway create")
    
    if success:
        print("✅ Railway project created!")
        print("🌐 Deploying...")
        run_command("railway up")
        print("✅ Deployed to Railway!")
        return True
    else:
        print(f"❌ Railway deployment failed: {error}")
        return False

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🟪 Deploying to Heroku...")
    
    # Check Heroku CLI
    success, _, _ = run_command("heroku --version")
    if not success:
        print("❌ Heroku CLI not installed. Please install from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    
    if app_name:
        create_cmd = f"heroku create {app_name}"
    else:
        create_cmd = "heroku create"
    
    print("🔐 Logging in to Heroku...")
    run_command("heroku login")
    
    print("📦 Creating Heroku app...")
    success, output, error = run_command(create_cmd)
    
    if success:
        print("✅ Heroku app created!")
        print("🌐 Deploying...")
        run_command("git add .")
        run_command('git commit -m "Deploy to Heroku"')
        run_command("git push heroku main")
        
        # Set environment variables
        run_command("heroku config:set ENV=production")
        run_command("heroku config:set HOST=0.0.0.0")
        
        print("✅ Deployed to Heroku!")
        return True
    else:
        print(f"❌ Heroku deployment failed: {error}")
        return False

def main():
    print("🚀 DataFixer Auto-Deploy Script")
    print("=" * 40)
    
    if not check_requirements():
        sys.exit(1)
    
    print("\nChoose deployment platform:")
    print("1. Railway (Recommended - Free & Easy)")
    print("2. Heroku (Popular)")
    print("3. Show manual instructions")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        deploy_to_railway()
    elif choice == "2":
        deploy_to_heroku()
    elif choice == "3":
        print("\n📖 Manual deployment instructions:")
        print("See DEPLOYMENT.md for detailed instructions")
        print("Quick links:")
        print("- Railway: https://railway.app")
        print("- Heroku: https://heroku.com")
        print("- Render: https://render.com")
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main()