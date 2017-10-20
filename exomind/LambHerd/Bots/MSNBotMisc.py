
"""
Based On
http://codemagnet.blogspot.com/2008/07/python-fun-project-msn-chat-bot.html
Marcus Low of malaysia :
"""


import time, string

def log_msg(md, email, type, msg, mtime = 0, users = []):
    """Logs the message or event of the 'type', related to 'email',
    with the content 'msg', to a file in the specified directory.  See
    documentation for more specific details, specially about
    formatting."""
    prepend = ''
    
    if users:
        # copy and sort the user list, so we log always to the same
        # file regarding the order the users were joined
        # FIXME: sometimes we crash because filename is too long
        usorted = users[:]
        usorted.sort()
        file = md.glob_config['history directory'] + '/' + prepend + 'MSG'
        file += string.join(usorted, ',')
        file2 = md.glob_config['history directory2'] + '/' + prepend + 'MSG'
        file2 += string.join(usorted, ',')
    else:
        file = md.glob_config['history directory'] + '/' + prepend + email
        file2 = md.glob_config['history directory2'] + '/' + prepend + email
    if not mtime:
        mtime = time.time()
    out = ''
    out += time.strftime('%d/%b/%Y %H:%M:%S ', time.localtime(mtime))
    out += email + ' '
    if type == 'in':
        out += '<<< '
        msg = msg.replace('\r', '')
        lines = msg.split('\n')
        if len(lines) == 1:
             out += msg + '\n'
        else:
            out += '\n\t'
            out += string.join(lines[:], '\n\t')
            out += '\n'
    elif type == 'out':
        out += '>>> ' + msg + '\n'
    elif type == 'status':
        out += '*** ' + msg + '\n'
    elif type == 'multi':
        out += '+++ ' + msg + '\n'
    elif type == 'realnick':
        out += '--- ' + msg + '\n'

    try:
        fd = open(file, 'a')
    except:
        fd = open(file2, 'a')	
    fd.write(out)
    fd.close()
    del(fd)
    return

#===================================================================================================#

def now():
    "Returns the current time, in tuple format"
    return time.localtime(time.time())

#===================================================================================================#

def email2nick(md, email):
    "Returns a nick accoriding to the given email, or None if noone matches"
    if email in md.users.keys():
        return md.users[email].nick
    else:
        return None

#===================================================================================================#

def print_inc_msg(md, email, lines, eoh = 0, quiet = 0, ptime = 1, recvtime = 0):
    """Prints an incoming message from a list of lines and an optional
    end-of-header pointer.  You can also pass the original received time as
    a parameter, this is used for history printed."""
    nick = email2nick(md, email)
    if not nick: nick = email
    if email in md.glob_ignored:
        return
    if ptime:
        if recvtime:
            ctime = time.strftime('%I:%M:%S%p', time.localtime(recvtime))
        else:
            ctime = time.strftime('%I:%M:%S%p', now())
        if md.debug_flag:
            print('%s ' % ctime)
    if md.debug_flag:
        print('%s' % nick)
    if len(lines[eoh:]) == 1:
        if md.debug_flag:
            print(' <<< %s\n' % lines[eoh])
    else:
        if md.debug_flag:
            print(' <<< \n\t')
        msg = string.join(lines[eoh:], '\n\t')
        msg = msg.replace('\r', '')
        if md.debug_flag:
            print(msg + '\n')
    beep(quiet)

#===================================================================================================#

def print_out_msg(nick, msg):
    "Prints an outgoing message"
    ctime = time.strftime('%I:%M:%S%p', now())    
#    print('%s ' % ctime)
#    print('%s' % nick)
#    print(' >>> ')
#    print('%s' % msg)

#===================================================================================================#

def beep(q = 0):
    "Beeps unless it's told to be quiet"
    if not q:
        print('\a')
        
#===================================================================================================#

