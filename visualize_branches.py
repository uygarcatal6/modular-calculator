#!/usr/bin/env python3
import subprocess
import re
from collections import defaultdict

def get_git_info():
    """Get git log information with detailed formatting."""
    try:
        # Get detailed git log
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline', '--graph', '--decorate', 
             '--pretty=format:%h|%d|%s|%an|%ar'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_branches():
    """Get all branches with their info."""
    try:
        result = subprocess.run(
            ['git', 'branch', '-vv'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_commits_for_branch(branch):
    """Get commits in a branch."""
    try:
        result = subprocess.run(
            ['git', 'log', f'{branch}', '--oneline', '-10'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.stdout
    except Exception as e:
        return ""

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def main():
    print("\n")
    print_header("📊 GIT BRANCH VISUALIZATION")
    
    # Show all branches
    print("🌿 ALL BRANCHES:")
    print("-" * 70)
    branches_info = get_branches()
    if branches_info:
        for line in branches_info.strip().split('\n'):
            if line.strip():
                # Highlight current branch
                if line.startswith('*'):
                    print(f"  ➤ {line}  ⭐ CURRENT")
                else:
                    print(f"    {line}")
    
    # Show graph
    print_header("📈 COMMIT GRAPH")
    git_log = get_git_info()
    if git_log:
        print(git_log)
    
    # Show detailed commit info
    print_header("📝 RECENT COMMITS DETAILS")
    try:
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline', '-15'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        for i, line in enumerate(result.stdout.strip().split('\n'), 1):
            if line.strip():
                parts = line.split(' ', 1)
                commit_hash = parts[0]
                message = parts[1] if len(parts) > 1 else ""
                
                # Color coding by feature
                emoji = "✨"
                if "power" in message.lower():
                    emoji = "⚡"
                elif "trigo" in message.lower() or "sin" in message.lower() or "cos" in message.lower():
                    emoji = "🔢"
                elif "fix" in message.lower():
                    emoji = "🐛"
                elif "chore" in message.lower():
                    emoji = "🧹"
                
                print(f"  {i:2d}. {emoji} {commit_hash[:7]} - {message}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Show what's in each branch
    print_header("🎯 BRANCH CONTENTS")
    branches = []
    try:
        result = subprocess.run(
            ['git', 'branch', '-a'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        for line in result.stdout.strip().split('\n'):
            branch = line.replace('*', '').replace('HEAD ->', '').strip()
            if branch and not branch.startswith('remotes'):
                branches.append(branch)
    except:
        pass
    
    for branch in branches:
        print(f"\n📌 Branch: {branch}")
        print("-" * 70)
        commits = get_commits_for_branch(branch)
        if commits:
            for line in commits.strip().split('\n')[:5]:
                if line.strip():
                    print(f"    • {line}")
        else:
            print("    (no commits)")
    
    print_header("✅ SUMMARY")
    print(f"Total branches: {len(branches)}")
    print("\nMajor features added:")
    print("  • ⚡ Power operator (**) - Math operations")
    print("  • 🔢 Trigonometric functions (sin, cos) - Advanced math")
    print("  • 🎯 Parentheses support ( ) - Expression grouping")
    print("\n")

if __name__ == "__main__":
    main()
