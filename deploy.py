#!/usr/bin/env python3
"""
Deployment helper script for Background Remover App
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def check_git_status():
    """Check if git repository is ready for deployment"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes:")
            print(result.stdout)
            return False
        return True
    except subprocess.CalledProcessError:
        print("❌ Git repository not found or not initialized")
        return False
    except FileNotFoundError:
        print("❌ Git not installed. Please install Git first.")
        return False

def show_deployment_options():
    """Show available deployment options"""
    print("🚀 Background Remover App - Deployment Options")
    print("=" * 50)
    print()
    
    print("1. 🎯 Railway (Recommended - Easiest)")
    print("   • Free tier available")
    print("   • Automatic deployment from GitHub")
    print("   • No configuration needed")
    print("   • Steps:")
    print("     a) Push to GitHub")
    print("     b) Connect to Railway")
    print("     c) Deploy automatically")
    print()
    
    print("2. 🌐 Render")
    print("   • Free tier available")
    print("   • Good for static sites")
    print("   • Easy GitHub integration")
    print()
    
    print("3. 🟣 Heroku")
    print("   • Popular platform")
    print("   • Requires Heroku CLI")
    print("   • Good documentation")
    print()
    
    print("4. 🐍 PythonAnywhere")
    print("   • Python-focused")
    print("   • Good for beginners")
    print("   • Manual file upload")

def setup_github():
    """Help setup GitHub repository"""
    print("\n📚 Setting up GitHub Repository")
    print("-" * 30)
    
    if not check_git_status():
        print("❌ Please commit your changes first:")
        print("   git add .")
        print("   git commit -m 'Your commit message'")
        return False
    
    print("✅ Git repository is ready!")
    print()
    print("Next steps:")
    print("1. Go to https://github.com and create a new repository")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print("   git remote add origin <your-repo-url>")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    
    return True

def railway_deployment():
    """Guide for Railway deployment"""
    print("\n🚂 Railway Deployment Guide")
    print("-" * 30)
    
    if not setup_github():
        return
    
    print("After pushing to GitHub:")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your repository")
    print("6. Railway will automatically:")
    print("   • Detect Python app")
    print("   • Install dependencies")
    print("   • Deploy your app")
    print("   • Provide a public URL")
    print()
    print("🎉 Your app will be live in minutes!")

def render_deployment():
    """Guide for Render deployment"""
    print("\n🎨 Render Deployment Guide")
    print("-" * 30)
    
    if not setup_github():
        return
    
    print("After pushing to GitHub:")
    print("1. Go to https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your repository")
    print("5. Configure:")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: gunicorn app:app")
    print("6. Deploy!")
    print()
    print("🎉 Your app will be live!")

def open_deployment_guides():
    """Open deployment guides in browser"""
    guides = {
        "Railway": "https://railway.app",
        "Render": "https://render.com",
        "Heroku": "https://devcenter.heroku.com/articles/getting-started-with-python",
        "PythonAnywhere": "https://help.pythonanywhere.com/pages/Flask/"
    }
    
    print("\n🌐 Opening deployment guides...")
    for platform, url in guides.items():
        print(f"Opening {platform} guide...")
        webbrowser.open(url)

def main():
    """Main deployment helper"""
    print("🎨 Background Remover App - Deployment Helper")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Show deployment options")
        print("2. Setup GitHub repository")
        print("3. Railway deployment guide")
        print("4. Render deployment guide")
        print("5. Open all deployment guides in browser")
        print("6. Check git status")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "1":
            show_deployment_options()
        elif choice == "2":
            setup_github()
        elif choice == "3":
            railway_deployment()
        elif choice == "4":
            render_deployment()
        elif choice == "5":
            open_deployment_guides()
        elif choice == "6":
            check_git_status()
        elif choice == "0":
            print("👋 Good luck with your deployment!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
