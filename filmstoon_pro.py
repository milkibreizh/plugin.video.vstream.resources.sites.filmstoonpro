# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# TODO : resources/art/sites  https://www.filmstoon.pro/templates/filmstoon/images/logo.webp
# 3
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress#, VSlog



SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Filmstoon pro'
SITE_DESC = ' films en streaming'

URL_MAIN = 'https://www.filmstoon.pro/'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    
    liste = []
    
    liste.append(['Action', URL_MAIN + 'film/action/'])
    liste.append(['Animation', URL_MAIN + 'film/anime/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'film/arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'film/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'film/biopic/'])
    liste.append(['Comédie', URL_MAIN + 'film/comedie/'])
    liste.append(['Comédie dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Documentaire', URL_MAIN + 'film/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'film/drame/'])
    liste.append(['Epouvante-horreur', URL_MAIN + 'film/epouvante-horreur/'])
    liste.append(['Espionnage', URL_MAIN + 'film/espionnage'])
    liste.append(['Famille', URL_MAIN + 'film/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'film/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'film/guerre/'])
    liste.append(['Historique', URL_MAIN + 'film/historique/'])
    liste.append(['Musical', URL_MAIN + 'film/musical/'])
    liste.append(['Policier', URL_MAIN + 'film/policier/'])
    liste.append(['Romance', URL_MAIN + 'film/romance/'])
    liste.append(['Science fiction', URL_MAIN + 'film/science-fiction/'])
    liste.append(['Thriller', URL_MAIN + 'filmthriller/'])
    liste.append(['Western', URL_MAIN + 'film/western/'])
    
    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch: 
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler( )
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<h2> <span>Film Streaming.+?href="(.+?)">(.+?)<.+?data-src="(.+?)".+?st-desc">(.+?)<.div'
    #g1:url  g2:title g3:thumb g4:desc

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)      
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break        
            sUrl   = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]  
            sDesc  = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)  
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        NextPage = __checkForNextPage(sHtmlContent)
        if (NextPage != False):
            sNumLastPage  = NextPage[0]
            sUrlNextPage = NextPage[1]     
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlNextPage)   
            number = re.search('/page/([0-9]+)', sUrlNextPage ).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number +'/'+ sNumLastPage +' >>>[/COLOR]', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]*)<.a><.span>\s*<span class="pnext.+?href="([^<]*)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if (aResult[0] == True):
        return aResult[1][0]
    return False 

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    #sDesc = oInputParameterHandler.getValue('sDesc')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'iframe src="data:image.+?show.filmstoon.pro.+?php.([^"]*)&'
    
    # g1 : parametres de la requete que l'on va copier et echanger 
    # avec celle genérée normalement par https://easyplayer.cc/player.php? 
    # c'est quasiment la meme 
    
    requestlist=[] 
    oParser = cParser() 
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    
    if (aResult[0] == True): 
        
        for aEntry in aResult[1]:        
            req = 'https://easyplayer.cc/player.php?'+str(aEntry )
            requestlist.append(req)
            
    for irequest in requestlist :
        #  url du host dans l'entete de la réponse
        urlreq = irequest
        oRequestHandler = cRequestHandler(urlreq)                
        oRequestHandler.request()
        sHeader=oRequestHandler.getResponseHeader()
         
        for iheader in sHeader:
            if iheader == 'refresh':
                sHosterUrl = sHeader.getheader('refresh')               
                sHosterUrl = sHosterUrl.split(';') 
                sHosterUrl = sHosterUrl[1]
                sHosterUrl = sHosterUrl.replace('url=','')            
                break    
        
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    
    oGui.setEndOfDirectory()

