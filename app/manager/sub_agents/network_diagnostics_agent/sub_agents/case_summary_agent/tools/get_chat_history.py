from ........app.main import session_service

def get_chat_history():
    """
    Retrieve the chat history from the session service.
    
    Returns:
        list: A list of chat messages in the session.
    """
    session = session_service.get_session()

    if not session:
        return []

    # Assuming session.messages contains the chat history
    chat_history = session.messages if hasattr(session, 'messages') else []
    
    return chat_history