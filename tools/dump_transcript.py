import json

log_path = '/Users/mettamazza/.gemini/antigravity/brain/a46b735c-f7e4-40e7-ae81-c95c7bc7d24f/.system_generated/logs/transcript_full.jsonl'
out_path = '/Users/mettamazza/Desktop/Smithian Fold Theory/Google Deepminds Science enclosure and AI misalignment.md'

with open(out_path, 'w', encoding='utf-8') as f_out:
    f_out.write('# Complete Turn-by-Turn Transcript of Session\n\n')
    f_out.write('This document contains the unedited turn-by-turn transcript of this session, extracted directly from the system logs to ensure a complete recount without evasion or summarization.\n\n')
    
    with open(log_path, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            if not line.strip(): continue
            try:
                data = json.loads(line)
                step_type = data.get('type', '')
                source = data.get('source', '')
                content = data.get('content', '')
                
                if step_type == 'USER_INPUT' and content:
                    f_out.write(f'## User\n\n{content}\n\n---\n\n')
                elif source == 'MODEL' and content:
                    f_out.write(f'## AI Assistant\n\n{content}\n\n---\n\n')
            except Exception as e:
                pass
