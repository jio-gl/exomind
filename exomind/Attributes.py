

class Attributes:
    
    TAG_ATTR = 'TAG'
    URL_SOURCE_ATTR = 'URL_SOURCE'
    WEIGHT_ATTR = 'WEIGHT'
    EMAIL_ATTR = 'EMAIL'
    
    ALIAS_ATTR = 'ALIAS'
    
    YOUTUBE_ALIAS_ATTR = 'YOUTUBE_ALIAS'
    FLICKR_ALIAS_ATTR = 'FLICKR_ALIAS'
    TWITTER_ALIAS_ATTR = 'TWITTER_ALIAS'
    SEARCHENGINEBOT_ALIAS_ATTR = 'SEARCHENGINEBOT_ALIAS'
    FACEBOOK_ALIAS_ATTR = 'FACEBOOK_ALIAS'
    LINKEDIN_ALIAS_ATTR = 'LINKEDIN_ALIAS'
    
    PLOT_COLORS = {
                   YOUTUBE_ALIAS_ATTR:'#FE3333',
                   FLICKR_ALIAS_ATTR:'#FF0084',
                   TWITTER_ALIAS_ATTR:'#86FF7F',
                   SEARCHENGINEBOT_ALIAS_ATTR:'#5ACB5A',
                   LINKEDIN_ALIAS_ATTR:'#8FFFE8',
                   FACEBOOK_ALIAS_ATTR:'#3b5998',
                   }

    
    @classmethod
    def choose_node_color(cls, type):
        if type in cls.PLOT_COLORS:
            return cls.PLOT_COLORS[type]
        else:
            return None
    
