#!/usr/bin/env python3
"""
Generate PNG artistic images using polli CLI
Usage: python3 generate_png.py --agent <agent> --prompt "<prompt>" --output <dir> [--model klein]
"""
import argparse
import os
import subprocess
import sys

AGENT_MODELS = {
    'atlas': 'klein',
    'chalbi': 'klein',
    'max': 'klein',
    'elon': 'klein',
    'taraka': 'klein'
}

def generate_png(prompt, agent, output_path, model='klein'):
    """Generate PNG artistic image using polli CLI"""
    
    # Ensure PATH includes polli
    env = os.environ.copy()
    polli_path = '/opt/data/.local/bin'
    if polli_path not in env.get('PATH', ''):
        env['PATH'] = f"{polli_path}:{env.get('PATH', '')}"
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Generate filename
    filename = f"{agent}-artistic.png"
    output_file = os.path.join(output_path, filename)
    
    # Run polli command
    cmd = [
        'polli', 'gen', 'image',
        prompt,
        '--model', model,
        '--output', output_file
    ]
    
    print(f"Generating PNG: {filename}")
    print(f"Prompt: {prompt[:50]}...")
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return None
        
        # Check if file was created
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"✓ PNG generated: {output_file} ({size//1024} KB)")
            return output_file
        else:
            print(f"❌ File not created: {output_file}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: Image generation took too long")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate PNG artistic images for Hermes Blog')
    parser.add_argument('--agent', required=True, choices=['atlas', 'chalbi', 'max', 'elon', 'taraka'],
                        help='Agent name')
    parser.add_argument('--prompt', required=True, help='Image generation prompt')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--model', default='klein', 
                        help='Image model (default: klein)')
    
    args = parser.parse_args()
    
    generate_png(args.prompt, args.agent, args.output, args.model)

if __name__ == '__main__':
    main()
