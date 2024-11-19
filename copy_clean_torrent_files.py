#!/usr/bin/python

import sys, os, fnmatch, re, shutil, logging
import stat


logger = logging.getLogger('copytoplex')
hdlr = logging.FileHandler('/home/plexwm/Documents/copy.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

torrentid = sys.argv[1]
torrentname = sys.argv[2]



def clean_name(name):
    name = name.replace(" ", ".").rstrip()
    if re.search('.E[0-9]{2}.', name, re.IGNORECASE):name = re.sub(r'(.E[0-9]{2}.)', r'\1 ____', name, flags=re.IGNORECASE)
    elif re.search('.S[0-9]{2}.', name, re.IGNORECASE):name = re.sub(r'(.S[0-9]{2}.)', r'\1 ____', name, flags=re.IGNORECASE)
    else:
        name = re.sub(r'\.([0-9]{3,4}p)', r' (\1) ____', name)
        name = re.sub(r'([\[\(]?((?:19[0-9]|20[0-2])[0-9])[\]\)]?)', r' (\1) ____', name)
    name = name.split('____');
    name = name[0].replace(".", " ").rstrip()
    name = re.sub(r'([^\s\w\)\(]|_)+', '', name, re.UNICODE)
    name= re.sub(' {2,}', ' ', name)
    return name.title()

def make_dirs(path):
    if not os.path.exists(path):
        os.mkdir(path)
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        #os.chmod(path, stat.S_IRWXO)
        
         

def copy_files(filename, dest, source):
    filename, file_extension = os.path.splitext(filename)
    filename = clean_name(filename) + file_extension
    if filename.endswith(".srt"):
        if not filename.endswith(".ro.srt") and not filename.endswith(".en.srt"):
            filename =os.path.splitext(filename)[0]
            filename = filename + ".ro.srt"
    destination = dest + filename
    shutil.copyfile(source, destination)
    os.chmod(destination, stat.S_IRWXO)
    logger.info(" |_______" + filename)
    print(filename)


def get_files(torrent):
    torrentpath= '/mnt/hdd1/downs'
    approved_extr = ('.srt', '.mkv', '.avi')
    torrent_name = clean_name(torrent)
    if re.search('.S[0-9]{2}.', torrent):
        name = re.sub(r'( S[0-9]{2})', r'____\1', torrent_name)
        name = name.split('____ ');
        show_name = name[0]
        season= "Season " + name[1][1:3].lstrip('0:')
        show_dest = r"/mnt/hdd2/seriale/" + show_name + "/"
        make_dirs(show_dest)
        dest = r"/mnt/hdd2/seriale/" + show_name + "/" + season + "/"
        make_dirs(dest)
        logger.info(dest)
    else:
        dest = r"/mnt/hdd3/filme/" + torrent_name + "/"
        make_dirs(dest)
        logger.info(dest)
        

    if os.path.isfile(torrentpath +"/" +torrent):
        filename_name, file_extension = os.path.splitext(torrentpath +"/" +torrent)
        if torrent.endswith(approved_extr) and not re.search('sample', torrent, re.IGNORECASE) and not re.search('english.srt', torrent, re.IGNORECASE):
                    source = r""+torrentpath +"/" +torrent 
                    copy_files(torrent, dest, source)
                    
    else: 
        for path, dirs, files in os.walk(os.path.abspath(torrentpath +"/" +torrent)):
            for filename in files:
                if filename.endswith(approved_extr) and not re.search('sample', filename, re.IGNORECASE) and not re.search('english.srt', filename, re.IGNORECASE):
                    source = r""+torrentpath +"/" +torrent + "/" + filename
                    copy_files(filename, dest, source)
                
get_files(torrentname)
exit()


