#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""BetaPy - Librairie python pour Betaseries

Projet-url: http://betapy.googlecode.com

"""

import urllib
import urllib2
import hashlib
import urlparse
import json


class Beta:
    def __init__( self,
                  key="a71be26370dc",
                  user_agent="BetaPy",
                  format="json",
                  login=None,
                  password=None):
        """Initialisation des paramètres.
        
        Possibilités de spécifier:
          * une clé api individuelle
          * l'user-agent pour les requêtes
.          * le format souhaité pour les retours de requêtes (xml ou json). Par
            défaut, le format de retour est un dictionnaire python.

        Pour définir le token une seule fois, l'attribuer à l'instance de Beta.
        Exemple:
          beta = betapy.Beta(login="dev001", password="developer")
          auth = beta.members_auth()
          token = auth['member']['token']
          beta.token = token
          print beta.planning_member()
        
        """
        #Type element
        self.type=["episode", "show", "member", "movie"]
        self. order = ["desc","asc"]
        self.binary = [0,1]
        # définition de la clé API utilisateur.
        self.key = str(key)
        # définition de l'User-Agent pour les requêtes
        self.user_agent = str(user_agent)
        # definition du format des retours de requêtes
        self.format = format
        # définition des identifiants de l'utilisateur
        self.login = login
        self.password = password
        # instanciation de la classe Builder pour le traitement des requêtes
        self.build = Builder(self.key, self.user_agent, self.format)
        # le token est à attribué lors à l'instanciation de la class Beta
        self.token = None
    
    def post_comments_comment(self, token, type, id, text, in_reply_to = None):
        """
        type:self.type  id:int, text:string, in_reply_to:int
        """
        if id == None or text == None or (type not in self.type):
            ##TODO
            return None
        params = urllib.urlencode({'token':token})
        values = {'type': type, 'id': id, 'text': text}
        if in_reply_to is not None:
            values['in_reply_to']=in_reply_to
        post_params = urllib.urlencode(values)       
        url = self.build.url("/comments/comment", params, True)
        return self.build.data(url, post_params)        
    
    def comments_comments(self, type, id, ndpp, since_id = None, order ="asc", replies=1):
        """
        type: self.type, id: int, ndpp: int > 0, since_id:int, order: self.order, replies: self.binary
        """
        if (type not in self.type) or (order not in self.order) or (replies not in self.binary):
            ##TODO
            return None
        dict_values = {'type': type, 'id': id, 'ndpp': ndpp, 'order': order, 'replies': replies}
        if since_id is not None:
            dict_values['since_id']=since_id
        params = urllib.urlencode(dict_values)
        url = self.build.url("/comments/comments", params)
        return self.build.data(url)
    
    def comments_replies(self, id, ordre="asc"):
        """
        id: int, type: self.order
        """
        if (ordre not in self.order):
            return None ##TODO
        params = urllib.urlencode({'id': id, 'order':ordre})
        url = self.build.url("/comments/replies", params)
        return self.build.data(url)
        
    def comments_subscription_post(self, token, type, id):
        """
        token: token connexion, type: self.type, id:integer
        """
        if type not in self.type:
            return None
        params = urllib.urlencode({'token': token})
        post_params = urllib.urlencode({'type': type, 'id': id})
        url = self.build.url("/comments/subscription", params, True)
        return self.build.data(url, post_params)
    
    def episodes_display(self, id = [], thetvdb_id = [], subtitles = True):
        """
        id
        """
        if (len(id) + len(thetvdb_id)) == 0:
            print "at least, one array between id and thetvdb_id must be not empty !"
            return None
        dict_params = {}        
        if (len(id) > 0):
            dict_params['id'] = str(id).strip('[]').replace(" ", "")
        if (len(thetvdb_id) > 0):
            dict_params['thetvdb_id'] = str(thetvdb_id).strip('[]').replace(" ", "")
        dict_params['subtitles'] = str(subtitles).lower()
        params = urllib.urlencode(dict_params)
        url = self.build.url("/episodes/display", params)
        return self.build.data(url)        
    
    def episodes_downloaded_post(self, token, id = None, tvdb_id = None):
        """
        id:integer, tvdb_id: integer, One of them must be declared
        """
        if id is None and tvdb_id is None:
            return None ##TODO
        params = urllib.urlencode({'token': token})
        post_values={}
        if id is not None:
            post_values['id']=id
        if tvdb_id is not None:
            post_values['thetvdb_id']=tvdb_id
        post_params = urllib.urlencode(post_values)
        url = self.build.url("/episodes/downloaded", params, True)
        return self.build.data(url, post_params)
        
    def episodes_list(self, subtitles = "all", limit = None, showId = None, userId = None, token = None):
        dict_params = {}
        if userId is not None:
            dict_params['userId']= userId
        if showId is not None:
            dict_params['showId']= showId
        if token is not None:
            dict_params['token']= token
        if limit is not None:
            dict_params['limit']= limit
        dict_params['subtitles']= subtitles
        params = urllib.urlencode(dict_params)
        url = self.build.url("/episodes/list", params)
        return self.build.data(url)
        
    def episodes_note_post(self, token, note, id=None, thetvdb_id=None):
        """
        note:0<note<5, id:int, thetvdb_id:int
        """
        if ((note < 0) or (note > 5) or ((id is None) and (thetvdb_id is None))):
            return None ##TODO
        params = urllib.urlencode({'token' : token})
        post_values={'note':note}
        if id is not None:
            post_values['id']=id
        if thetvdb_id is not None:
            post_values['thetvdb_id']=thetvdb_id        
        post_params = urllib.urlencode(post_values)
        url = self.build.url("/episodes/note", params, True)
        return self.build.data(url, post_params)
    
    ##TOFIX    
    def episodes_scraper(self, file):
    	params = urllib.urlencode({'file':file.replace(" ", "+")})
        url = self.build.url("/episodes/scraper", params)
        print url
        return self.build.data(url)

    def episodes_search(self, show_id, number, subtitles=False):
        """
        show_id:int, number:int, subtitles:boolean
        """
    	params = urllib.urlencode({'show_id':show_id, 'number': number})
        url = self.build.url("/episodes/search", params)
        #print url
        return self.build.data(url)

        
    def members_auth(self):
        """Identifie le membre avec son login et le hash MD5.

        Retourne le token à utiliser pour les requêtes futures.

        """
        # hash MD5 du mot de passe
        hash_pass = hashlib.md5(self.password).hexdigest()
        # paramètres de l'url
        params = urllib.urlencode({})
        post_params = urllib.urlencode({'login': self.login, 'password': hash_pass})
        url = self.build.url("/members/auth", params)
        return self.build.data(url, post_params)        

    def members_episodes(self, token):
        """Vérifie si le token spécifié est actif."""
        return self.episodes_list(token=token)

    def members_infos(self, token=None, login=None):
        """Renvoie les informations principales du membre identifié ou d'un autre membre."""
        # si le nom d'un utilisateur est fourni, on ajoute le paramètre
        params = urllib.urlencode({'token': token})
        url = self.build.url("/members/infos", params)
        #print url
        return self.build.data(url)

    def movies_random(self, nb=1):
        params = urllib.urlencode({'nb': nb})
        url = self.build.url("/movies/random", params)
        return self.build.data(url)

    def planning_member(self, token="", view=""):
        """Affiche le planning du membre identifié ou d'un autre membre.
        
        L'accès varie selon les options vie privée de chaque membre).
        Vous pouvez rajouter le paramètre view pour n'afficher que les épisodes encore non-vus.

        """
        params = urllib.urlencode({'token': token,'view' : view})
        url = self.build.url("/planning/member", params)
        return self.build.data(url)
        
    def show_list(self, order = None, since = None):
        """
        Get the list of show sort by order defines as arg 
        (alphabetical, popularity, followers -> optionnal) 
        and since timestamp UNIX given (optionnal)
        """
        args = {}
        if order is not None:
            args['order'] = order
        if since is not None:
            args['since'] = since
        params = urllib.urlencode(args)
        url = self.build.url("/shows/list", params)
        return self.build.data(url)
                        
        
    def show_similar(self, id_show):
        """
        Get the similar show from the show given in arg
        """    
        params = urllib.urlencode({'id': id_show})
        url = self.build.url("/shows/similars", params)
        #print url
        return self.build.data(url)

    def subtitles_episode(self, id, language='all'):
        """
        Show the subtitle for the episode identified by the id
        """
        params = urllib.urlencode({'id': id, 'language': language})
        url = self.build.url("/subtitles/episode", params)
        return self.build.data(url)

class Builder:
    """Ensemble de fonctions utiles pour le traitement des requêtes vers l'API.
    
    Fonctionnalités:
      * Construction des url.
      * Récupération du contenu des requêtes.
      * Traitement des requêtes.

    """
    def __init__(self,
                 key=None,
                 user_agent=None,
                 format=None):
        """Initialisation des paramètres."""
        # définition de la clé API utilisateur.
        self.key = key
        # définition de l'User-Agent pour les requêtes
        self.user_agent = user_agent
        # definition du format des retours de requêtes
        self.format = format
	# Verison of the API used
	self.version = "2.2"
	

    def url(self, method, params=None, https=False):
        """Constructeur d'url pour les requêtes vers l'API.

        Exemple:
        >>> self.build_url("/members/auth", "login=Dev001&password=hash_md5")
        http://api.betaseries.com/members/auth.json?key=3c5b...&login=Dev001&password=5e8...

        """

        scheme = 'http'
	if https:
		scheme = 'https'
        # url de l'api
        netloc = 'api.betaseries.com'
	path = method
        # insertion de la clé api
        param_key = "key=%s&v=%s" % (self.key, self.version)
        # construction des paramètres de l'url
        query = '%s&%s' % (param_key, params)
        # retourne l'ensemble de l'url
        return urlparse.urlunparse((scheme, netloc, path,
                                    None, query, None))

    def get_source(self, url):
        """Retourne le contenu renvoyé à partir d'une requête url.

        La fonction permet également de créer l'user-agent.

        """
        opener = urllib2.build_opener()
        # ajout de l'user-agent
        opener.addheaders = [('User-agent', self.user_agent)]
	if self.format == 'json':
		opener.addheaders = [('Accept', "application/json")]
	else:
		opener.addheaders = [('Accept', "text/xml")]
        source = opener.open(url)
        # retourne le contenu
        return source.read()

    def get_post_source(self, url, postparams):
        """Retourne le contenu renvoyé à partir d'une requête url.
        La fonction permet également de créer l'user-agent.
        """
	req = urllib2.Request(url, postparams)
	response = urllib2.urlopen(req)
	return response.read()

    def data(self, url, postparams=None):
        """Converti les retours de requêtes en données communément exploitables.

        Proposition: tout transformer en dictionnaire python par défaut.
        
        Si l'utilisateur souhaite le retour en xml ou en json, il est retourné

        """
        # récupération du contenu à partir d'une requête url
        if postparams is not None:
            post = True
        else:
            post = False
	source = None
	handler=urllib2.HTTPHandler(debuglevel=1)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)
	if post:
		source = self.get_post_source(url, postparams)
	else:
	        source = self.get_source(url)
        # si le format de retour souhaité est le json ou xml
        if self.format in ['xml', 'json']:
            return source
        # si l'utilisateur n'a pas entré de format OU souhaite un dictionnaire
        else:
            json_data = json.loads(source)
            # retourne le contenu sous forme de dictionnaire Python
            return json_data
