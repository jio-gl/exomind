
from exomind.Utils import normalize_token

import re

class EmailHarvestingCommand:

    __forb_tags = ['the', 'and', 'their', 'at', 'is', 'in', 'of', 
                   'a', 'on', 'for', 'an', 'with', 'to', 'this', 'mail', 'lo', 'was', 'than']    
    
    __only_complete_names = False

    __grab_types = [
                    'domain2name&email',
                    'name2email&domain',
                    'name2anyemail&domain',
                    'email2name&email'
                    'email2anyname&email'
                    ]
    
    def __init__(self):
        pass
        
    def set_grab_type(self, grab_type):
        self.__grab_type = grab_type
    
    def set_only_complete_names(self, flag):
        self.__only_complete_names = flag
    
    def get_inputs(self, node):
        grab_type = self.__grab_type        
        # convert urls and inputs to list removing spaces.
        if grab_type == 'name2email&domain' or grab_type == 'name2anyemail&domain':
            if len(node.strip().split()) < 2:
                print 'Warning: only complete name with first and last name is possible input: %s' % node.strip()
                return []
            inputs = []
            i = node
            # first.last
            inputs.append( i.strip().lower().replace(' ', '.') )
            # first_last
            inputs.append( i.strip().lower().replace(' ', '_') )
            # firstlast
            inputs.append( i.strip().lower().replace(' ', '') )
            first = i.strip().lower().split(' ')[0]
            last  = i.strip().lower().split(' ')[1]
            # first_firstletterlast
            #inputs.append( first[0] + last )
            if grab_type == 'name2email&domain':
                grab_type = 'email2name&email'
            else:
                grab_type = 'email2anyname&email'
                
        else:            
            inputs = [node.strip()]

        self.__grab_type = grab_type
        return inputs

    def get_regexes(self, input):
        grab_type = self.__grab_type
        # inputs is a list containing the end of the email addresses to search
        # i.e. name@domain

        nonvc = r'[^/=!\"#$%(),:;<>@[\\\]\'|\s\t\n\r\f\v]+'  # non-valid address characters
        # matches: (case doesn't matter)
        #           name@example.com
        #           name@example.com.ar
        #           name@ar.example.com
        #           name at example.com
        #           name at example dot com
        #           name&#64example.com
        #           name@<b>example.com</b>
        #           name at <b>example.com</b>
        #           name&#64<b>example dot com</b>
        regexps = []
        # types are 'domain2name&email' 'email2name&name'
        if grab_type == 'domain2name&email':
            # the following urls should NOT contain groups
            regexps += [
                                # first_name last_name bla@example.com
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at ' + input,
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at ' + input.replace('.',' dot '),
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'&#64;' + input,
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'@(?:\w+[_\-\.]{1})*' + input + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with input between <b> and </b>
                                # (yahoo puts search pattern between them)
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at <b>' + input + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'&#64;<b>' + input + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'@(?:\w+[_\-\.]{1})*<b>' + input + r'</b>(?:[_\-\.]{1}\w+)*',

                                # bla@example.com
                                nonvc + r' at ' + input,
                                nonvc + r' at ' + input.replace('.',' dot '),
                                nonvc + r'&#64;' + input,
                                nonvc + r'@(?:\w+[_\-\.]{1})*' + input + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with input between <b> and </b>
                                # (yahoo puts search pattern between them)
                                nonvc + r' at <b>' + input + r'</b>',
                                nonvc + r'&#64;<b>' + input + r'</b>',
                                nonvc + r'@(?:\w+[_\-\.]{1})*<b>' + input + r'</b>(?:[_\-\.]{1}\w+)*'
                             ]
        elif grab_type == 'email2name&email':
            # the following urls should NOT contain groups
            regexps += [
                                # first_name last_name bla@example.com
                                nonvc + r' ' + nonvc + r' ' + input + r' at ' + nonvc,
                                nonvc + r' ' + nonvc + r' ' + input + r' at ' + nonvc + r' dot ' + nonvc + r' ',
                                nonvc + r' ' + nonvc + r' ' + input + r'&#64;' + nonvc,
                                nonvc + r' ' + nonvc + r' ' + input + r'@(?:\w+[_\-\.]{1})*' + nonvc + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with input between <b> and </b>
                                # (yahoo puts search pattern between them)
                                nonvc + r' ' + nonvc + r' ' + input + r' at <b>' + nonvc + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + input + r'&#64;<b>' + nonvc + r' dot ' + nonvc + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + input + r'@(?:\w+[_\-\.]{1})*<b>' + nonvc + r'</b>(?:[_\-\.]{1}\w+)*',

                                # bla@example.com
                                input + r' at ' + nonvc,
                                input + r' at ' + nonvc + r' dot ' + nonvc + r' ',
                                input + r'&#64;' + nonvc,
                                input + r'@(?:\w+[_\-\.]{1})*' + nonvc + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with input between <b> and </b>
                                # (yahoo puts search pattern between them)
                                input + r' at <b>' + nonvc + r'</b>',
                                input + r'&#64;<b>' + nonvc + r' dot ' + nonvc + r'</b>',
                                input + r'@(?:\w+[_\-\.]{1})*<b>' + nonvc + r'</b>(?:[_\-\.]{1}\w+)*'
                             ]
        elif grab_type == 'email2anyname&email':
            # the following urls should NOT contain groups
            regexps += [
                                # first_name last_name bla@example.com
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at ' + nonvc,
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at ' + nonvc + r' dot ' + nonvc + r' ',
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'&#64;' + nonvc,
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'@(?:\w+[_\-\.]{1})*' + nonvc + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with nonvc between <b> and </b>
                                # (yahoo puts search pattern between them)
                                nonvc + r' ' + nonvc + r' ' + nonvc + r' at <b>' + nonvc + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'&#64;<b>' + nonvc + r' dot ' + nonvc + r'</b>',
                                nonvc + r' ' + nonvc + r' ' + nonvc + r'@(?:\w+[_\-\.]{1})*<b>' + nonvc + r'</b>(?:[_\-\.]{1}\w+)*',

                                # bla@example.com
                                nonvc + r' at ' + nonvc,
                                nonvc + r' at ' + nonvc + r' dot ' + nonvc + r' ',
                                nonvc + r'&#64;' + nonvc,
                                nonvc + r'@(?:\w+[_\-\.]{1})*' + nonvc + r'(?:[_\-\.]{1}\w+)*',
                                # same as above but with nonvc between <b> and </b>
                                # (yahoo puts search pattern between them)
                                nonvc + r' at <b>' + nonvc + r'</b>',
                                nonvc + r'&#64;<b>' + nonvc + r' dot ' + nonvc + r'</b>',
                                nonvc + r'@(?:\w+[_\-\.]{1})*<b>' + nonvc + r'</b>(?:[_\-\.]{1}\w+)*'
                             ]
        else:
            raise Exception("ERROR: bad grab_type")
        return regexps

    def purify_matches(self, matches):
            if matches == []:
                return []
            emails = {}
            # forbiden string in 'first_name last_name'
            forbiden_subtrings = ['escribi', 'resumes', 'write', 'email', 'cv ', 'comments', 'e-mail', 'contact', 'support', 'him ', 'please', ' from']
            forbiden_suffixes = [' to', ' list', ' lists', ' as', ' a']
            # normalize found addresses
            for email in matches:
                # convert result to lowercase, since the DB is case insensitive
                email = email.lower()

                # replace ' at ' with '@' and ' dot ' with '.'
                email = email.replace(' at ', '@').replace(' dot ', '.')
                # remove <b> and </b> tags
                email = email.replace('<b>', '').replace('</b>', '')
                # replace '&#64;' with '@'
                email = email.replace('&#64;', '@')
                
                if len(re.findall('@', email)) > 1:
                    continue
                s = email.split(' ')
                if len(s) > 1: # has first_name last_name
                    names = s[:2]
                    email = ' '.join(s[2:])
                    # if mail has no dots is a bad email
                    for forb in forbiden_subtrings:
                        if forb in ' '.join(names):
                            names = []
                    for forb in forbiden_suffixes:
                        if ' '.join(names).endswith(forb):
                            names = []
                    # no numbers
                    if re.search('[0-9]+', ' '.join(names)):
                        names = []
                else:
                    names = []
                    email = ' '.join(s)

                if email.endswith('.'):
                    email = email[:-1]
                email = email.replace('&gt','')
                
                if (names == [] or '.' in ' '.join(names)) and self.__only_complete_names:
                    continue
                if len(names) > 0 and names[0] in self.__forb_tags:
                    continue
                if len(names) > 1 and names[1] in self.__forb_tags:
                    continue

                email = normalize_token(email)
                if not '...' in email:
                    if not email in emails or emails[email] == '':
                        if len(email.split(u'@')[-1].split(u'.')) < 2 or email.endswith(u'.'): 
                            continue
                        emails[email] = ' '.join(names)
                elif self.__canFixEmail(email, names):
                    email = self.__fixEmail(email, names)
                    if not email in emails or emails[email] == '':
                        if len(email.split(u'@')[-1].split(u'.')) < 2 or email.endswith(u'.'): 
                            continue
                        emails[email] = ' '.join(names)

            pair_list = []
            for row, name in emails.iteritems():      # hack to show table
                try:
                    # now we have tuples (name,email)s
                    row = (row,name.replace('.', '').strip())
                    #print(str(row))
                    pair_list.append(row)
                except Exception, e:
                    print 'Ignoring email address. Contains invalid characters.'                    
                    
            # remove things like ('pperez@bla.com', '') if ('pperez@bla.com', 'Pirulo Perez') exists 
            return pair_list

    def __canFixEmail(self, email, names):
        ret = len(names)>0 and (len(email.split('@')[0]) == len('.'.join(names)) or len(email.split('@')[0]) == len(names[1]) or len(email.split('@')[0]) == len(names[0]) or len(email.split('@')[0]) == len(names[1])+1)
        return len(names)>0 and (len(email.split('@')[0]) == len('.'.join(names)) or len(email.split('@')[0]) == len(names[1]) or len(email.split('@')[0]) == len(names[0]) or len(email.split('@')[0]) == len(names[1])+1)

    def __fixEmail(self, email, names):
        if len(email.split('@')[0]) == len('.'.join(names)):
            # fix with first_name.last_name@example.com
            ret = '.'.join(names).lower() + '@' + email.split('@')[1]
            return '.'.join(names).lower() + '@' + email.split('@')[1]
        elif len(email.split('@')[0]) == len(names[1])+1:
            # fix with only first_name_one_letterlast_name@example.com
            ret = names[0].lower()[0:1] + names[1].lower() + '@' + email.split('@')[1]
            return names[0].lower()[0:1] + names[1].lower() + '@' + email.split('@')[1]
        elif len(email.split('@')[0]) == len(names[0]):
            # fix with only first_name@example.com
            ret = names[0].lower() + '@' + email.split('@')[1]
            return names[0].lower() + '@' + email.split('@')[1]
        else:
            # fix with only last_name@example.com
            ret = names[1].lower() + '@' + email.split('@')[1]
            return names[1].lower() + '@' + email.split('@')[1]


