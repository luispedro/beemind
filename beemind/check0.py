def check_inbox0(server, username, password, mailbox='INBOX'):
    '''
    Checks (using IMAP) if an inbox is empty
    '''
    import imaplib
    conn = imaplib.IMAP4_SSL(server)
    conn.login(username, password)
    conn.select(mailbox)
    results, data = conn.search(None, 'ALL')
    data = data[0]
    return len(data) == 0
