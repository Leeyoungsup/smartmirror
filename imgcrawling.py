import urllib.request

url = "http://post.phinf.naver.net/20151210_93/yesfile_jj_1449716137622Hp5qh_JPEG/mug_obj_144971614855130099.jpg"

savename ='Mountain.jpg'

urllib.request.urlretrieve(url, savename)
print('save..........')


