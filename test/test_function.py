#! /usr/bin/env python

import betapy
import json
import urllib2
import MySQLdb
import argparse	
debug_all = False
debug_similar = False
debug_subtitle = False
debug_ended = False
debug_list_show = False
debug_export_file = False
debug_episodes_display = False
debug_episodes_list = False
debug_movies_random = False
debug_comments_comment_post = False
debug_comments_comment = False
debug_comments_replies = False
debug_comments_subscription_post = False
debug_episodes_downloaded_post = False
debug_episodes_note_post = False
debug_episodes_scraper = True
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
	token  = authRes['token']
	to_see = json.loads(beta.members_infos(token))
        shows = []
        similar_show = {}
        id_title = {}
	for show in to_see['member']['shows']:
                shows.append(show['id'])
                if show['status'] == 'Ended' and not show['user']['archived']:
                        if debug_ended or debug_all:
                                print show['title']
	if debug_similar or debug_all:
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
        if debug_subtitle or debug_all:
                print '############################'                
                print json.loads(beta.subtitles_episode(192197))                
        if debug_list_show or debug_all:
                print '############################'                
                shows_list = json.loads(beta.show_list())                
                print shows_list
                if debug_export_file:
                        f = open("series.json", "w")
                        f.write(str(shows_list))
                        f.close()
        if debug_episodes_display or debug_all:
                print '###########################'        
                print json.loads(beta.episodes_display(id=[192197,192198]))	
        if debug_episodes_list or debug_all:
                print '###########################'        
                print json.loads(beta.episodes_list(token=token))
                print json.loads(beta.members_episodes(token=token))
        if debug_movies_random or debug_all:
                print '###########################'        
                print json.loads(beta.movies_random())
        if debug_comments_comment_post or debug_all:
		print '###########################'        
                print json.loads(beta.post_comments_comment(token, "show", 2410, "Hello World"))
        if debug_comments_comment or debug_all:
		print '###########################'        
		if debug_all:
		        if json.loads(beta.comments_comments("show", 2410, 20)) is not None:
		                print "comments_comment OK"
                else:
                        print json.loads(beta.comments_comments("show", 2410, 20))
        if debug_comments_replies or debug_all:
                print '###########################'        
                if debug_all:
                        if json.loads(beta.comments_replies(35981)) is not None:
                                print "comments_replies OK"
                else:
                        print json.loads(beta.comments_replies(35981))
        if debug_comments_subscription_post or debug_all:
                print '###########################'
                if debug_all:
                        if json.loads(beta.comments_subscription_post(token, "show", 2410)) is not None:
                                print "comments_suscribtion_post OK"
                else:
                        print json.loads(beta.comments_subscription_post(token, "show", 2410))
        if debug_episodes_downloaded_post or debug_all:
                print '###########################'
                if debug_all:
                        if json.loads(beta.episodes_downloaded_post(token, 233264)) is not None:
                                print "episodes_downloaded ok"
                else:
                        print json.loads(beta.episodes_downloaded_post(token, 233264))
        if debug_episodes_note_post or debug_all:
                print '###########################'
                if debug_all:
                        if json.loads(beta.episodes_note_post(token, 4, 233264)) is not None:
                                print "episodes_note_post ok"
                else:
                        print json.loads(beta.episodes_note_post(token, 4, 233264))
        if debug_episodes_scraper or debug_all:
                print '###########################'
                if debug_all:
                        if json.loads(beta.episodes_scraper("lostgirlS01E01")) is not None:
                                print "episodes_scraper ok"
                else:
                        print json.loads(beta.episodes_scraper("lostgirlS01E01"))
if __name__ == "__main__":
	main()