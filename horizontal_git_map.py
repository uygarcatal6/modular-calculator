#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def get_git_log():
    """Get detailed git log."""
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

def generate_horizontal_mindmap():
    """Generate horizontal mind map visualization."""
    commits = get_git_log()
    
    # Sort by date
    commits_sorted = sorted(commits, key=lambda x: x['date'])
    
    def get_color(message):
        if 'power' in message.lower() or '**' in message:
            return '#FFD700'
        elif 'trigo' in message.lower() or 'sin' in message.lower() or 'cos' in message.lower():
            return '#87CEEB'
        elif 'C-button' in message or 'clear' in message.lower():
            return '#FF6347'
        elif 'fix' in message.lower():
            return '#FF69B4'
        elif 'chore' in message.lower():
            return '#90EE90'
        else:
            return '#B0C4DE'
    
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
    <title>Yatay Git Haritası - Modular Calculator</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
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
            overflow-x: auto;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            position: sticky;
            top: 0;
            background: rgba(102, 126, 234, 0.9);
            padding: 15px;
            border-radius: 10px;
            z-index: 100;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 0.95em;
            opacity: 0.95;
        }
        
        .timeline-wrapper {
            display: flex;
            align-items: center;
            gap: 0;
            overflow-x: auto;
            padding: 40px 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            scroll-behavior: smooth;
        }
        
        .timeline-scroll {
            display: flex;
            gap: 30px;
            min-width: 100%;
            padding: 0 50px;
        }
        
        .time-column {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            min-width: 200px;
            position: relative;
        }
        
        .time-column::after {
            content: '';
            position: absolute;
            right: -15px;
            top: 50%;
            width: 30px;
            height: 3px;
            background: linear-gradient(90deg, #667eea, transparent);
            transform: translateY(-50%);
        }
        
        .time-column:last-child::after {
            display: none;
        }
        
        .time-label {
            font-size: 0.85em;
            color: #999;
            font-weight: bold;
            text-align: center;
            width: 100%;
        }
        
        .commits-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 100%;
        }
        
        .commit-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 15px;
            border-left: 5px solid;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .commit-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .commit-card:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }
        
        .commit-icon {
            font-size: 1.8em;
            margin-bottom: 5px;
            display: block;
            text-align: center;
        }
        
        .commit-hash {
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #667eea;
            font-weight: bold;
            text-align: center;
        }
        
        .commit-message {
            font-size: 0.9em;
            color: #333;
            margin: 8px 0;
            font-weight: 500;
            text-align: center;
            line-height: 1.3;
        }
        
        .commit-author {
            font-size: 0.75em;
            color: #666;
            text-align: center;
        }
        
        .refs-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.7em;
            margin-top: 5px;
            text-align: center;
            width: 100%;
            font-weight: bold;
        }
        
        .mindmap-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .mindmap-container h2 {
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
            font-size: 1.5em;
        }
        
        .mindmap {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            min-height: 300px;
        }
        
        .branch-node {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .branch-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            animation: float 3s ease-in-out infinite;
            font-size: 1.1em;
            text-align: center;
            padding: 15px;
        }
        
        .branch-circle:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        }
        
        .branch-circle.main {
            background: linear-gradient(135deg, #667eea, #764ba2);
            width: 180px;
            height: 180px;
            font-size: 1.3em;
            z-index: 10;
        }
        
        .branch-circle.feature {
            background: linear-gradient(135deg, #87CEEB, #4169E1);
            width: 120px;
            height: 120px;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        .legend {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .legend-text {
            font-size: 0.9em;
            color: #333;
        }
        
        .scroll-hint {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 10px 15px;
            border-radius: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            font-size: 0.85em;
            color: #667eea;
            font-weight: bold;
            animation: pulse 2s infinite;
            z-index: 50;
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
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
            <h1>📊 Git Commit Timeline - Yatay Zihin Haritası</h1>
            <p>⏱️ Sol → Sağ: Zamanda İleriye Doğru</p>
        </div>
        
        <div class="timeline-wrapper" id="timelineWrapper">
            <div class="timeline-scroll" id="timelineScroll">
"""
    
    # Group commits by date
    from collections import defaultdict
    commits_by_date = defaultdict(list)
    
    for commit in commits_sorted:
        date_obj = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
        date_key = date_obj.strftime('%d.%m.%Y')
        commits_by_date[date_key].append(commit)
    
    # Generate timeline
    for date_key in sorted(commits_by_date.keys()):
        commits_on_date = commits_by_date[date_key]
        html += f"""
                <div class="time-column">
                    <div class="time-label">{date_key}</div>
                    <div class="commits-group">
"""
        
        for commit in commits_on_date[:3]:  # Max 3 commits per day
            color = get_color(commit['message'])
            icon = get_icon(commit['message'])
            refs_html = ""
            if commit['refs']:
                refs_html = f'<div class="refs-badge">{commit["refs"].strip()}</div>'
            
            message = commit['message'][:30] + '...' if len(commit['message']) > 30 else commit['message']
            
            html += f"""
                        <div class="commit-card" style="border-left-color: {color};">
                            <span class="commit-icon">{icon}</span>
                            <div class="commit-hash">{commit['hash_short']}</div>
                            <div class="commit-message">{message}</div>
                            <div class="commit-author">{commit['author'][:15]}</div>
                            {refs_html}
                        </div>
"""
        
        html += """
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="mindmap-container">
            <h2>🧠 Branch Mind Map</h2>
            <div class="mindmap">
                <div class="branch-node">
                    <div class="branch-circle feature">
                        feature/c-button<br/>
                        🗑️
                    </div>
                </div>
                
                <div class="branch-node">
                    <div class="branch-circle main">
                        🌿 master<br/>
                        (CURRENT)
                    </div>
                </div>
                
                <div class="branch-node">
                    <div class="branch-circle feature">
                        feature/trigo<br/>
                        🔢 sin/cos
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mindmap-container">
            <h2>🎨 Renk Tanımlaması</h2>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #FFD700;"></div>
                    <span class="legend-text">⚡ Power Operator</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #87CEEB;"></div>
                    <span class="legend-text">🔢 Trigonometric</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF6347;"></div>
                    <span class="legend-text">🗑️ Clear Button</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF69B4;"></div>
                    <span class="legend-text">🐛 Fixes</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #90EE90;"></div>
                    <span class="legend-text">🧹 Chore</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #B0C4DE;"></div>
                    <span class="legend-text">✨ Other</span>
                </div>
            </div>
        </div>
        
        <div class="scroll-hint">
            👉 Yatay kaydır →
        </div>
        
        <footer>
            <p>🚀 Git Yatay Harita Görselleştirmesi | Modular Calculator</p>
        </footer>
    </div>
    
    <script>
        // Smooth scroll
        const timelineScroll = document.getElementById('timelineScroll');
        const timelineWrapper = document.getElementById('timelineWrapper');
        
        timelineWrapper.addEventListener('wheel', (e) => {
            e.preventDefault();
            timelineWrapper.scrollLeft += e.deltaY;
        });
        
        // Animate cards on load
        const cards = document.querySelectorAll('.commit-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 50);
        });
        
        // Add hover effect
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.zIndex = '10';
            });
            card.addEventListener('mouseleave', function() {
                this.style.zIndex = '1';
            });
        });
        
        // Remove scroll hint after first scroll
        let scrolled = false;
        timelineWrapper.addEventListener('scroll', () => {
            if (!scrolled) {
                scrolled = true;
                document.querySelector('.scroll-hint').style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""
    
    return html

def main():
    html = generate_horizontal_mindmap()
    
    output_file = "horizontal_git_map.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Yatay harita oluşturuldu: {output_file}")
    print(f"📖 Browser'da açılıyor...")
    
    # Try to open in browser
    import os
    import webbrowser
    try:
        abs_path = os.path.abspath(output_file)
        webbrowser.open(f'file://{abs_path}')
        print("🌐 Browser'da açıldı!")
    except:
        print(f"📁 Dosya: {output_file}")

if __name__ == "__main__":
    main()
