#! /usr/bin/env python

import betapy
import json
import urllib2
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
	#beta = betapy.Beta(login="nogebour", password="jv99xkzz", format='json')
	authRes = json.loads(beta.members_auth())
	#print authRes
	to_see = json.loads(beta.members_infos(authRes['token']))
        shows = []
        similar_show = {}
        id_title = {}
	for show in to_see['member']['shows']:
                shows.append(show['id'])
                if show['status'] == 'Ended' and not show['user']['archived']:
                        print show['title']
	for show_id in shows:
                try:
	                similar = json.loads(beta.show_similar(show_id))
                except urllib2.HTTPError:
                        similar=None
                if not similar is None:
        	        for show in similar['similars']:
        	                id_title[show['show_id']]=show['show_title']
                                if not show['show_id'] in shows:
        	                        if not show['show_id'] in similar_show.keys():
                                                similar_show[show['show_id']] = 0
                                        similar_show[show['show_id']] +=1
        print '############################'
        sorted_list = [(k,v) for v,k in sorted([(v,k) for k,v in similar_show.items()])]
        for dis_show in sorted_list:
                print id_title[dis_show[0]]+" -> "+str(dis_show[1])
                
        	
		
if __name__ == "__main__":
	main()