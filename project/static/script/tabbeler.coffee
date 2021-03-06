

#'hidethings' hides all the things with kword. I's pretty much replaced by 'deletethings'
hidethings= (kword) ->
    things = document.getElementsByClassName(kword)
    for thing in things
        thing.style.visibility="hidden"


# Do you have class? Sorry... this is a boolean for testing if an element has some classname. It is used in 'deletethings'.
hasClass = ( target, className ) ->
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className)

# this deletes all elements with class kword, except ones with class "Main"
deletethings= (kword) ->
    things = document.getElementsByClassName(kword)
    for i in [things.length-1...-1]
        if ! hasClass(things[i], "Main")
            things[i].parentElement.removeChild(things[i])


# This gets all the title and body of all elements with kword.
#Returns a nice formatted array.
## maybe in the future it will take an array like ["title", "body"] to make it more modular.
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


#  WELL.... This is for getting querystrings. I may use it sometime.... just not now.
#The god of mixed javascript and coffeescript is pleased.
`
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
//I pulled this from here: http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
// Thanks stack overflow user "jolly.exe"
`

`
function inittab(){
        if(window.location.hash){
            var goo = $('#tabs div ul li');
            for (var i = 0; i<goo.length; i++){
                if('#'+goo[i].textContent==window.location.hash){
                    console.log(goo[i].textContent+" is the best at space");
                    $(goo[i]).addClass('active');
                }else{
                    $(goo[i]).removeClass('active');
                }
            }
        }else{
		$('#tabs article:first').show();
		$('#tabs div ul li:first').addClass('active');
        }
}
`
#And now for the main event!
class window.tabbeler

    datalist: []

    constructor: (contentname) ->
        @contentname = contentname


    htmltabme: () ->
        this.datalist = gettitandbod(this.contentname)
        deletethings(this.contentname)
        #document.getElementById("TextsMain").style.visibility="visible"
        this.body = document.getElementsByClassName("Main body")[0]
      # If this.body does not get defined then it must not exist. So we don't do anything.
        if this.body
             this.body.style.visibility="visible"
            # If the url has a fragment identifier show the text named by it.
             if window.location.hash
                 this.showtabcontent(window.location.hash.substring(1))
             else
                 this.body.innerHTML = this.datalist[0][1]

        $('#tabs div ul li a').on 'click', (event) =>
            thing = $(event.target)
            this.showtabcontent(thing[0].innerHTML)
            $('#tabs div ul li').removeClass('active')
            thing.parent().addClass('active')
            thing.parent().show()

        inittab()



    showtabcontent: (name)->
        for i in [0...this.datalist.length]
            if this.datalist[i][0]==name
                this.body.innerHTML=this.datalist[i][1]

