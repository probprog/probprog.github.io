all: deploy

deploy: build
	git stash
	(cd _site && tar cf ../website.tar .)
	git checkout master
	-mkdir  anglican
	(cd anglican && tar xvf ../website.tar)
	git add anglican
	-git commit -a -m 'updated anglican website'
	-git push
	git checkout development
	git stash pop

build:
	-rm website.tar
	jekyll build
