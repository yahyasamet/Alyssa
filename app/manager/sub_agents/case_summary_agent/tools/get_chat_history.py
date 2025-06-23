import glob

def get_chat_history():
    
    chat_history = []
    
    # Get all conversation files in the current directory
    conversation_files = glob.glob("conversation_*.txt")
    
    for file_path in conversation_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                chat_history.append({
                    'file': file_path,
                    'content': content
                })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return chat_history