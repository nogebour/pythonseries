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

def main():
	args=args_space()
	beta = betapy.Beta(login=args.login, password=args.password, format='json')
	authRes = json.loads(beta.members_auth())
	to_see = json.loads(beta.members_infos(authRes['token']))
        shows = []
        id_title = {}
	for show in to_see['member']['shows']:
                shows.append(show['id'])
                if show['status'] == 'Ended' and not show['user']['archived']:
                        print show['title']                
        	
		
if __name__ == "__main__":
	main()