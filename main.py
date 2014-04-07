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

def main():
	args=args_space()
	beta = betapy.Beta(login=args.login, password=args.password, format='json')
	conn = MySQLdb.connect(host="localhost", user="betapy", passwd="", db="betapy")
	c = conn.cursor()
	try:
		authRes = json.loads(beta.members_auth())
		#print authRes['user']['id']
		to_see = json.loads(beta.members_episodes(authRes['token']))
		count = 0
		for show in to_see['shows']:
			count +=show['remaining']
		print count
		c.execute("INSERT INTO global_remain(day, count) VALUES (CURDATE(), %s)" % (count))
		#print sort_shows(to_see)
		id_title, id_remaining = struct_datas(to_see)
		for id_show, name in id_title.iteritems():
			c.execute("SELECT id FROM tvshow WHERE id=%s;" % (id_show))
			if c.fetchone() is None:
				c.execute("INSERT INTO tvshow(id, name) VALUES (%s, \"%s\");" % (id_show, name))
		for remain, shows in id_remaining.iteritems():
			for one_show in shows: 
				#print "Hello"
				c.execute("INSERT INTO stats_show(id, day,remaining) VALUES (%s, CURDATE(), %s);" % (one_show, remain))
		#conn.commit()
		conn.close()
	except urllib2.HTTPError, err:
		print "Error"
		
if __name__ == "__main__":
	main()