

hidethings= (kword) ->
    things = document.getElementsByClassName(kword)
    for thing in things
        thing.style.visibility="hidden"


hasClass = ( target, className ) ->
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className)

# this deletes all elements with class kword, except ones with class "Main"
deletethings= (kword) ->
    things = document.getElementsByClassName(kword)
    for i in [things.length-1...-1]
        if ! hasClass(things[i], "Main")
            things[i].parentElement.removeChild(things[i])

gettitandbod= (kword) ->
    titles = document.getElementsByClassName("#{kword} title")
    bodies = document.getElementsByClassName("#{kword} body")
    if titles.length!=bodies.length
        console.log "Something went wrong. There are not the same amount of titles as of body texts"
        return []
    datas = []
    for i in [0...titles.length]
        datas.push([titles[i].innerHTML,bodies[i].innerHTML])
    return datas

class window.tabbeler

    datalist: []

    constructor: (contentname) ->
        @contentname = contentname

    htmltabme: () ->
        this.datalist = gettitandbod(this.contentname)
        deletethings(this.contentname)
        #document.getElementById("TextsMain").style.visibility="visible"
        this.body = document.getElementsByClassName("Main body")[0]
        this.body.style.visibility="visible"
        this.body.innerHTML = this.datalist[0][1]

    showtabcontent: (name)->
        for i in [0...this.datalist.length]
            if this.datalist[i][0]==name
                this.body.innerHTML=this.datalist[i][1]

