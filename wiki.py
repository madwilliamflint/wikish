#
import bottle
import wikistorage

# Display the page list if no page is specified.
@bottle.route('/wiki')
@bottle.route('/wiki/')
def todo_list():
    return show_page('FrontPage')
    pagelist = wikistorage.page_list()
    output = bottle.template('templates/wiki_pages.tpl',pagelist=pagelist)
    return str(output)

@bottle.route('/wiki/<pagename>')
@bottle.route('/wiki/<pagename>/')
def show_page(pagename):
    content = wikistorage.get_page(pagename)
    return bottle.template('templates/wiki_page.tpl',renderer=wikistorage.html_render,pagename=pagename,content=content)
    # If page exists: Display the page
    # If page does NOT exist: Display the edit page form (prepopulated Title)

@bottle.route('/wiki/edit/<pagename>', method='GET')
def edit_page(pagename):
    content = ''
    if wikistorage.page_exists(pagename):
        content = wikistorage.get_page(pagename)
    return bottle.template('templates/wiki_edit_page.tpl',pagename=pagename,body=content)

@bottle.route('/wiki/search/<pagename>')
def search_page(pagename):
    itemlist = wikistorage.get_backlinks(pagename)
    print itemlist
    return bottle.template('templates/wiki_search_results.tpl',pagename=pagename,items=itemlist)

@bottle.route('/wiki/save/<pagename>', method='POST')
def save_page(pagename):
    content = bottle.request.POST.content.strip()
    wikistorage.save_page(pagename,content)
    return show_page(pagename)

@bottle.route('/wiki/debug/pagelist/')
def page_list():
    return bottle.template('templates/wiki_pages.tpl',pagelist=wikistorage.page_list())

@bottle.route('/wiki/debug/allbacklinks/')
def all_backlinks():
    bl_content = wikistorage.get_all_backlinks()
    return bottle.template('templates/wiki_page.tpl',renderer=wikistorage.html_render,pagename='Backlinks',content=bl_content)


@bottle.error(500)
def mistake(code):
    return "Wow. You sure did SOMEthing wrong. I mean, or maybe it was me. I don't know. I'm not your mom; I'm just the generic 500 error message."

@bottle.error(403)
def mistake(code):
    return 'The parameter you passed has the wrong format!'

@bottle.error(404)
def mistake(code):
    return 'Whupsitude.'

bottle.debug(True)
bottle.run(host='0.0.0.0',port=8080,reloader=True)
