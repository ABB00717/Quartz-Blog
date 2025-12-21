import os
import re

TARGET_DIR = "/home/abb00717/Projects/abb00717.com/content/01-學術專區/作業系統"

def get_all_md_files(root_dir):
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def process_frontmatter(content):
    # Split by the first two ---
    # Be robust about whitespace
    parts = re.split(r'^---$', content, maxsplit=2, flags=re.MULTILINE)
    
    if len(parts) >= 3 and content.strip().startswith('---'):
        # Verify the first part is empty (before first ---)
        if parts[0].strip() == '':
            fm = parts[1]
            body = parts[2]
            
            # Check for tags
            if 'tags:' not in fm:
                # Add tags
                # Try to insert after draft or title, or just append
                if 'date:' in fm:
                     fm = fm.replace('date:', 'tags:\n  - operating-system\ndate:', 1)
                else:
                     fm = fm.rstrip() + "\ntags:\n  - operating-system\n"
            
            return fm, body
    
    # If no valid frontmatter found or format is different
    # Create simple frontmatter
    fm = "\ntitle: Untitled\ntags:\n  - operating-system\ndate: 2025-12-11\n"
    body = content
    return fm, body

def process_body(body):
    lines = body.split('\n')
    
    first_header_level = None
    for line in lines:
        m = re.match(r'^(#+)\s', line)
        if m:
            first_header_level = len(m.group(1))
            break
            
    # If the first header is H2 (##), promote all headers by one level
    if first_header_level == 2:
        promoted_lines = []
        for line in lines:
            if re.match(r'^#+\s', line):
                # Remove the first char which is '#'
                promoted_lines.append(line[1:])
            else:
                promoted_lines.append(line)
        lines = promoted_lines

    # REGEX for numbered headers: # 1. Title, ## 1.2 Title, 1\. Title, etc.
    # We want to match headers that start with a number.
    # Pattern: ^(#+)\s+(\d+(?:\\?\.\d+)*\\?\.?)\s+(.*)
    # Allows for optional backslash before dots.
    
    header_pattern = re.compile(r'^(#+)\s+(\d+(?:\\?\.\d+)*\\?\.?)\s+(.*)')
    
    cleaned_lines = []
    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Replace with # Title
            cleaned_lines.append(f"{match.group(1)} {match.group(3)}")
        else:
            cleaned_lines.append(line)
            
    # Now handle separators
    # We want a `---` before every H1 (`# `), unless it's the very start of the text.
    
    final_lines = []
    
    def is_hr(l):
        return bool(re.match(r'^[-*_]{3,}\s*$', l))

    skip_next = False
    
    for i, line in enumerate(cleaned_lines):
        if line.strip().startswith('# ') and not line.strip().startswith('##'):
            # It is H1
            
            # 1. Clean up preceding lines (remove empty lines and existing HRs to standardise)
            while final_lines and (not final_lines[-1].strip() or is_hr(final_lines[-1])):
                final_lines.pop()
                
            # 2. Decide if we need a separator
            # If final_lines is empty, it means this H1 is the first content. No separator.
            # If final_lines has content, add separator.
            
            if final_lines:
                final_lines.append("")
                final_lines.append("---")
                final_lines.append("")
            
            final_lines.append(line)
            
        elif is_hr(line):
            # Check if this HR is followed by an H1 (ignoring empty lines)
            # If so, we skip it because the H1 logic above handles insertion.
            # If not, we keep it (e.g. separator between normal paragraphs).
            
            is_followed_by_h1 = False
            for future_line in cleaned_lines[i+1:]:
                if not future_line.strip():
                    continue
                if future_line.strip().startswith('# ') and not future_line.strip().startswith('##'):
                    is_followed_by_h1 = True
                break
            
            if not is_followed_by_h1:
                final_lines.append(line)
        else:
            final_lines.append(line)
            
    return "\n".join(final_lines)

def main():
    files = get_all_md_files(TARGET_DIR)
    print(f"Found {len(files)} files.")
    
    for file_path in files:
        # print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        fm, body = process_frontmatter(content)
        new_body = process_body(body)
        
        # Reconstruct
        # Ensure new_body doesn't start with excessive newlines if body was trimmed
        new_body = new_body.strip()
        # Add one leading newline if needed to separate from ---
        new_body = "\n\n" + new_body + "\n"
        
        new_content = f"---\n{fm}\n---{new_body}"
        
        # Write back
        if new_content != original_content:
            print(f"Updating {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == "__main__":
    main()
