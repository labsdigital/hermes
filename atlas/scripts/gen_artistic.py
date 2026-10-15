#!/usr/bin/env python3
"""Generate artistic PNG for Atlas article about AI and emotion."""

import subprocess
import sys
import os

def main():
    output_path = "/opt/data/hermes/atlas/reports/emosi-ai-2026-10-07-artistik.png"
    
    prompt = """A surreal digital painting showing the boundary between human emotion and artificial intelligence. 
In the foreground, a human hand reaching out toward a glowing neural network that forms into a face. 
The neural network has warm golden and soft blue hues, representing simulated empathy. 
Behind the human hand, shadows of other humans fading into digital pixels. 
Style: dreamlike, ethereal, with soft lighting. 
Color palette: warm golds, soft blues, deep purples, and hints of white. 
Mood: contemplative, slightly melancholic but hopeful. 
Details: visible circuit patterns merging with organic forms, 
subtle binary code floating in the background, 
a single tear falling from the human hand turning into digital particles.
Artistic style inspired by sci-fi concept art and digital surrealism.
High quality, detailed, 4K resolution."""
    
    env = os.environ.copy()
    env["PATH"] = f"/opt/data/.local/bin:{env.get('PATH', '')}"
    
    try:
        result = subprocess.run(
            ["polli", "gen", "image", prompt, "--model", "klein", "--output", output_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            print(f"✅ Generated: {output_path}")
            print(f"Size: {os.path.getsize(output_path)} bytes")
            return 0
        else:
            print(f"❌ Failed: {result.stderr}")
            return 1
    except subprocess.TimeoutExpired:
        print("❌ Timeout generating image")
        return 1
    except FileNotFoundError:
        print("❌ polli not found")
        return 1

if __name__ == "__main__":
    sys.exit(main())
