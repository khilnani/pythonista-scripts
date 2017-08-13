from dulwich.repo import Repo
from dulwich.objects import Commit,Tree
import time
def find_lost_commits():
	r=Repo('.')
	o=r.object_store
	
	all_commits=[]
	all_trees=[]
	for sha in o:
		obj=o[sha]
		if isinstance(obj,Commit):
			all_commits.append(obj)
	
	#hide commits that have children, so we get "ends" of chains only
	for c in all_commits:
		for p in c.parents:
			try:
				all_commits.remove(p)
			except ValueError:
				pass
		if c.sha in r.get_refs().values():
			all_commits.remove(c)
	#hide commits that are in branches
	
	for c in sorted(all_commits,key=lambda x:x.commit_time):	
		print('{} {} {}'.format(time.ctime(c.commit_time),sha, c.message))

find_lost_commits
