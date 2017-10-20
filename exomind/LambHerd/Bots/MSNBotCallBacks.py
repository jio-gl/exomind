
"""
Based On
http://codemagnet.blogspot.com/2008/07/python-fun-project-msn-chat-bot.html
Marcus Low of malaysia :
"""

import time, string
from time import gmtime, strftime


from MSNBotMisc import *
import msnlib, msncb
import eliza

import urllib

# CALLBACKS

#===================================================================================================#

# user adds

def cb_add(md, type, tid, params):
    "Handles a user add; both you adding a user and a user adding you"
    t = params.split(' ')
    type = t[0]
    if type == 'RL':
        email = t[2]
        nick = urllib.unquote(t[3])
        msnlib.debug('ADD: %s (%s) added you' % (nick, email))
    elif type == 'FL':
        email = t[2]
        nick = urllib.unquote(t[3])
        gid = t[4]
        md.users[email] = msnlib.user(email, nick, gid)
        # put None in last_lst so BPRs know it's not coming from sync
        md._last_lst = None
        msnlib.debug('ADD: adding %s (%s)' % (email, nick))
    else:
        pass

# message

def cb_msg(md, type, tid, params, sbd):
    global last_received
    t = tid.split(' ')
    email = t[0]

    # parse
    lines = params.split('\n')
    headers = {}
    eoh = 0
    for i in lines:
        # end of headers
        if i == '\r':
            break
        tv = i.split(':', 1)
        type = tv[0]
        value = tv[1].strip()
        headers[type] = value
        eoh += 1
    eoh +=1

    # handle special hotmail messages
    if email == 'Hotmail':
        if not headers.has_key('Content-Type'):
            return
        hotmail_info = {}

        # parse the body
        for i in lines:
            i = i.strip()
            if not i:
                continue
            tv = i.split(':', 1)
            type = tv[0]
            value = tv[1].strip()
            hotmail_info[type] = value
        
        #msnlib.debug(params)
        if headers['Content-Type'] == 'text/x-msmsgsinitialemailnotification; charset=UTF-8':
            newmsgs = int(hotmail_info['Inbox-Unread'])
            if not newmsgs:
                return
            print('\rYou have %s unread email(s)' % str(newmsgs) \
                + ' in your Hotmail account\n')
        elif headers['Content-Type'] == 'text/x-msmsgsemailnotification; charset=UTF-8':
            from_name = hotmail_info['From']
            from_addr = hotmail_info['From-Addr']
            subject = hotmail_info['Subject']
            print('\rYou have just received an email in your' + \
                ' Hotmail account:\n')
            print('\r\tFrom: %s (%s)\n' % (from_name, from_addr))
            print('\r\tSubject: %s\n' % subject)
        return

    if headers.has_key('Content-Type') and headers['Content-Type'] == 'text/x-msmsgscontrol':
        # the typing notices
        nick = email2nick(md, email)
        if not nick: nick = email
        if not md.users[email].priv.has_key('typing'):
            md.users[email].priv['typing'] = 0
        if not md.users[email].priv['typing'] and email not in md.glob_ignored:
            print('\r')
            ctime = time.strftime('%I:%M:%S%p', now())
            print('%s ' % ctime)
            print('%s' % nick)
            print(' is typing\n')
        md.users[email].priv['typing'] = time.time()
    elif headers.has_key('Content-Type') and headers['Content-Type'] == 'text/x-clientcaps':
        # ignore the x-clientcaps messages generated from gaim
        pass
    elif headers.has_key('Content-Type') and headers['Content-Type'] == 'text/x-keepalive':
        # ignore kopete's keepalive messages
        pass
    else:
        # messages
        md.users[email].priv['typing'] = 0
        print('\r')
        print_inc_msg(md, email, lines, eoh)
        
        if len(sbd.emails) > 1:
            log_msg(md, email, 'in', string.join(lines[eoh:], '\n'), \
                users = sbd.emails)
        else:
            log_msg(md, email, 'in', string.join(lines[eoh:], '\n'))

        # append the message to the history, keeping it below the configured limit
        if len(md.glob_history_ring) > md.glob_config['history size']:
            del(md.glob_history_ring[0])
        md.glob_history_ring.append((time.time(), email, lines[eoh:]))
        
        chatline = lines[eoh:][0].strip()

        # print received msg
        tim = strftime("%a, %d %b %Y %H:%M:%S", gmtime())            
        print '(MSNBot) %s <<< %s: %s' % (tim, email, chatline)
        # restart initial_time
        md.initial_time = time.time()
        ans, quit = custom_chat_response(md, chatline)
        md.glob_quit = quit        
        if ans:
            tim = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            print '(MSNBot) %s >>> %s: %s' % (tim, email, ans)
            md.sendmsg(email, ans)

    last_received = email
    msncb.cb_msg(md, type, tid, params, sbd)
    
def custom_chat_response(md, chatline):    
    if md.auto_responses and md.auto_responses > 0:        
        print 'AUTO RESPONSE! (%d auto responses left) Wait...' % md.auto_responses
        md.auto_responses -= 1
        if md.chatbot_type == 'se':
            return md.sebot.reply_to(chatline), False 
        else:
            therapist = eliza.eliza()
            ans = therapist.respond(chatline).lower()
            return ans, False
    
    menu = '''
Choose: 
        a/auto -> for another automatic line of the chatbot.
        e -> one response from eliza
        m/manual -> for a manual chatline.
        c/cont <num> -> to continue with <num> chatbot lines.
        ec <num> -> to continue with <num> chatbot lines from eliza.
        q/quit-> quit chatbot.
        '''    
    ans, good, quit = None, False, False
    while not good:
        print menu
        input = raw_input()    
        if input.startswith('a') or input.startswith('auto'):
            print 'AUTO RESPONSE! Wait...'
            ans = md.sebot.reply_to(chatline)
            good = True
            md.chatbot_type = 'se'
        elif input.strip() == 'e':
            print 'AUTO RESPONSE! Wait...'
            therapist = eliza.eliza()
            ans = therapist.respond(chatline).lower()
            good = True
            md.chatbot_type = 'eliza'
        elif input.startswith('m') or input.startswith('manual'):
            print 'Insert manual chatline: '
            ans = raw_input()
            good = True
        elif input.startswith('c') or input.startswith('cont'):
            inputs = input.split(' ')
            md.auto_responses = int(inputs[1].strip())
            print 'AUTO RESPONSE! (%d auto responses left) Wait...' % md.auto_responses
            md.auto_responses = md.auto_responses - 1
            ans = md.sebot.reply_to(chatline)
            good = True
            md.chatbot_type = 'se'
        elif input.startswith('ec'):
            inputs = input.split(' ')
            md.auto_responses = int(inputs[1].strip())
            print 'AUTO RESPONSE! (%d auto responses left) Wait...' % md.auto_responses
            md.auto_responses = md.auto_responses - 1
            therapist = eliza.eliza()
            ans = therapist.respond(chatline).lower()
            good = True
            md.chatbot_type = 'eliza'
        elif input.startswith('q') or input.startswith('quit'):
            print 'QUITTING!'
            good = True
            quit = True
    return ans, quit

#===================================================================================================#
