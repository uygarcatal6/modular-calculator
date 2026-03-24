#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def get_git_log():
    """Get detailed git log as JSON-like format."""
    try:
        result = subprocess.run(
            ['git', 'log', '--all', '--pretty=format:%H|%h|%d|%s|%an|%ai|%ae'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                commits.append({
                    'hash_full': parts[0],
                    'hash_short': parts[1],
                    'refs': parts[2].strip(),
                    'message': parts[3],
                    'author': parts[4],
                    'date': parts[5],
                    'email': parts[6]
                })
        return commits
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_commits_by_branch():
    """Get commits grouped by branch."""
    try:
        # Get all branches
        result = subprocess.run(
            ['git', 'branch', '-a', '--format=%(refname:short)|%(objectname:short)'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        branches = {}
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                branch_name = parts[0]
                # Skip HEAD
                if 'HEAD' not in branch_name:
                    branches[branch_name] = parts[1] if len(parts) > 1 else ""
        return branches
    except:
        return {}

def generate_html():
    """Generate HTML visualization."""
    commits = get_git_log()
    branches = get_commits_by_branch()
    
    # Determine colors for different types
    def get_color(message):
        if 'power' in message.lower() or '**' in message:
            return '#FFD700'  # Gold
        elif 'trigo' in message.lower() or 'sin' in message.lower() or 'cos' in message.lower():
            return '#87CEEB'  # Sky blue
        elif 'C-button' in message or 'clear' in message.lower():
            return '#FF6347'  # Tomato
        elif 'fix' in message.lower():
            return '#FF69B4'  # Hot pink
        elif 'chore' in message.lower():
            return '#90EE90'  # Light green
        else:
            return '#B0C4DE'  # Light steel blue
    
    def get_icon(message):
        if 'power' in message.lower() or '**' in message:
            return '⚡'
        elif 'trigo' in message.lower() or 'sin' in message.lower() or 'cos' in message.lower():
            return '🔢'
        elif 'C-button' in message or 'clear' in message.lower():
            return '🗑️'
        elif 'fix' in message.lower():
            return '🐛'
        elif 'chore' in message.lower():
            return '🧹'
        else:
            return '✨'
    
    html = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Branch Visualization - Modular Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .branches-list {
            list-style: none;
        }
        
        .branches-list li {
            padding: 12px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .branch-name {
            font-weight: bold;
            color: #333;
        }
        
        .branch-type {
            font-size: 0.85em;
            color: #666;
            background: #e9ecef;
            padding: 3px 8px;
            border-radius: 3px;
        }
        
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 20px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #667eea, #764ba2);
        }
        
        .commit {
            margin-bottom: 25px;
            padding-left: 80px;
            position: relative;
        }
        
        .commit-dot {
            position: absolute;
            left: 8px;
            top: 5px;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            border: 3px solid white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            z-index: 1;
        }
        
        .commit-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .commit-box:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .commit-hash {
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #667eea;
            font-size: 0.9em;
        }
        
        .commit-message {
            color: #333;
            margin: 8px 0 5px 0;
            font-size: 0.95em;
        }
        
        .commit-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #666;
        }
        
        .commit-author {
            display: flex;
            align-items: center;
        }
        
        .commit-date {
            color: #999;
        }
        
        .refs {
            display: inline-block;
            padding: 2px 6px;
            background: #667eea;
            color: white;
            border-radius: 3px;
            font-size: 0.75em;
            margin: 0 3px;
            font-weight: bold;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 5px;
            color: white;
        }
        
        .badge-power {
            background: linear-gradient(135deg, #FFD700, #FFA500);
        }
        
        .badge-trigo {
            background: linear-gradient(135deg, #87CEEB, #4169E1);
        }
        
        .badge-clear {
            background: linear-gradient(135deg, #FF6347, #DC143C);
        }
        
        .badge-fix {
            background: linear-gradient(135deg, #FF69B4, #FF1493);
        }
        
        .badge-chore {
            background: linear-gradient(135deg, #90EE90, #32CD32);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .feature-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .feature-emoji {
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        .feature-title {
            font-weight: bold;
            color: #333;
        }
        
        .feature-desc {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧮 Modular Calculator</h1>
            <p>Git Branch Visualization & Commit History</p>
        </div>
        
        <div class="content">
            <div class="card">
                <h2>🌿 Branches</h2>
                <ul class="branches-list">
"""
    
    # Add branches
    for branch_name, commit_hash in sorted(branches.items()):
        branch_type = "remote" if "remotes" in branch_name else "local"
        icon = "📡" if branch_type == "remote" else "💻"
        html += f"""
                    <li>
                        <div>
                            <span>{icon} <span class="branch-name">{branch_name}</span></span>
                        </div>
                        <span class="branch-type">{commit_hash[:7]}</span>
                    </li>
"""
    
    html += """
                </ul>
            </div>
            
            <div class="card">
                <h2>📊 Statistics</h2>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">""" + str(len(commits)) + """</div>
                        <div class="stat-label">Total Commits</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">""" + str(len(branches)) + """</div>
                        <div class="stat-label">Branches</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">""" + str(len([c for c in commits if 'feat' in c['message'].lower()])) + """</div>
                        <div class="stat-label">Features</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>✨ Features Added</h2>
            <div class="features">
                <div class="feature-item">
                    <span class="feature-emoji">⚡</span>
                    <div class="feature-title">Power Operator (**))</div>
                    <div class="feature-desc">Mathematical exponentiation support</div>
                </div>
                <div class="feature-item">
                    <span class="feature-emoji">🔢</span>
                    <div class="feature-title">Trigonometric Functions</div>
                    <div class="feature-desc">sin() and cos() mathematical operations</div>
                </div>
                <div class="feature-item">
                    <span class="feature-emoji">🎯</span>
                    <div class="feature-title">Parentheses Support</div>
                    <div class="feature-desc">Expression grouping with ( )</div>
                </div>
                <div class="feature-item">
                    <span class="feature-emoji">🗑️</span>
                    <div class="feature-title">Clear Button</div>
                    <div class="feature-desc">Reset expression feature (C)</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📜 Commit Timeline</h2>
            <div class="timeline">
"""
    
    # Add commits
    for i, commit in enumerate(commits[:15]):
        color = get_color(commit['message'])
        icon = get_icon(commit['message'])
        refs_html = ""
        if commit['refs']:
            refs_html = f'<span class="refs">{commit["refs"].strip()}</span>'
        
        date_obj = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
        date_str = date_obj.strftime('%d.%m.%Y %H:%M')
        
        html += f"""
                <div class="commit">
                    <div class="commit-dot" style="background-color: {color};">{icon}</div>
                    <div class="commit-box" style="border-left-color: {color};">
                        <div class="commit-hash">{commit['hash_short']}</div>
                        <div class="commit-message">{commit['message']}</div>
                        {refs_html}
                        <div class="commit-meta">
                            <span class="commit-author">{commit['author']}</span>
                            <span class="commit-date">{date_str}</span>
                        </div>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <footer>
            <p>🚀 Generated by git visualization tool | Modular Calculator Project</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def main():
    html = generate_html()
    
    output_file = "branch_graph.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML visualization created: {output_file}")
    print(f"📖 Open it in your browser to see the visual git tree!")
    
    # Try to open in browser
    import os
    import webbrowser
    try:
        abs_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{abs_path}')
        print("🌐 Opening in browser...")
    except:
        print(f"📁 Manually open: {output_file}")

if __name__ == "__main__":
    main()
