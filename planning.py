#! /usr/bin/env python

import betapy
import json
import urllib2
import MySQLdb
import argparse	

def args_space():
	parser = argparse.ArgumentParser(description='Betaseries Authentification.')
	parser.add_argument('-l', '--login', type=str, required=True, help='Login for betaseries')
	parser.add_argument('-p', '--password', type=str, required=True, help='Password for Betaseries')      
	args = parser.parse_args()
	return args

def show_db(c, id_show, name):
	c.execute("SELECT id FROM tvshow WHERE id=%s;" % (id_show))
	#print "Add %s %s " % (id_show, name)
        if c.fetchone() is None:
        	#print "Hello"
	        c.execute("INSERT INTO tvshow(id, name) VALUES (%s, \"%s\");" % (id_show, name))

def episode_db(c, id_show, id_episode, code_ep, name, date):
	c.execute("SELECT id_ep FROM planning WHERE id_show=%s AND date_airing='%s' AND id_ep=%s;" % (id_show, date, id_episode))
	#print "Add %s %s " % (id_show, name)
        if c.fetchone() is None:
        	#print "%s %s %s " % (id_show, code_ep, date)
        	try:
		        c.execute("INSERT INTO planning(id_show, date_airing, id_ep, code_ep, title) VALUES (%s, \"%s\", %s, \"%s\", \"%s\");" % (id_show, date, id_episode, code_ep, name))
		except UnicodeEncodeError:        
			c.execute("INSERT INTO planning(id_show, date_airing, id_ep, code_ep) VALUES (%s, \"%s\", %s, \"%s\");" % (id_show, date, id_episode, code_ep))
	else:
		try:
		        c.execute("UPDATE planning SET title=\"%s\" WHERE date_airing=\"%s\" AND id_show=%s AND id_ep=%s;" % (name, date, id_show, id_episode))
		except UnicodeEncodeError:        
			print "Erreur title"
			#c.execute("INSERT INTO planning(id_show, date_airing, id_ep, code_ep) VALUES (%s, \"%s\", %s, \"%s\");" % (id_show, date, id_episode, code_ep))
			
def struct_datas(data):
	id_title = {}
	id_remaining = {}
	for show in data['shows']:
		#print str(show['id']) + " " + show['title'] + " " + str(show['remaining'])
		id_show = show['id']
		id_title[id_show] = show['title']
		if not show['remaining'] in id_remaining.keys():
			id_remaining[show['remaining']] = []
		id_remaining[show['remaining']].append(id_show)
	return id_title, id_remaining
	
def sort_shows(to_see):
	id_sort = []
	show_remain = {}
	id_title, id_remaining = struct_datas(to_see)
	keys = reversed(sorted(id_remaining.keys()))
	for key in keys:
		for show in id_remaining[key]:
			id_sort.append(id_title[show])
			show_remain[id_title[show]] = key
	return id_sort

def clear_planning(c, idepisodes):
        print "clear the DB"
        c.execute("SELECT id_ep, date_airing FROM planning;")
        s = c.fetchone()
        while not s is None:
                if not s[0] in idepisodes.keys():
                        c.execute("DELETE FROM planning WHERE id_ep = %s" % s[0])
                        print "Deleting of ep = %s" % (s[0])
                elif not (s[1] == idepisodes[s[0]]):
                        c.execute("DELETE FROM planning WHERE id_ep = %s AND date_airing = \"%s\"" % (s[0], s[1]))
                        print "Deleting of ep = %s" % (s[0])
                s = c.fetchone()

def main():
	args=args_space()
	beta = betapy.Beta(login=args.login, password=args.password, format='json')
	#beta = betapy.Beta(login="nogebour", password="jv99xkzz", format='json')
	conn = MySQLdb.connect(host="localhost", user="betapy", passwd="", db="betapy")
	c = conn.cursor()
	authRes = json.loads(beta.members_auth())
	#print authRes['user']['id']
	to_see = json.loads(beta.planning_member(authRes['token']))
	idep= {}
	for episode in to_see['episodes']:
	        #print episode['id']
		show_db(c, episode['show']['id'], episode['show']['title'])
		episode_db(c, episode['show']['id'], episode['id'], episode['code'], episode['title'], episode['date'])
		idep[episode['id']] = episode['date']
		conn.commit()
	clear_planning(c, idep)
	conn.commit()	
	#print to_see
	                                                        
	
		
if __name__ == "__main__":
	main()