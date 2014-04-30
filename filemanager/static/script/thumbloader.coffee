

class loadinglooper
    loopID: 0

    goloopy: () ->
        myID = thumbloader.loadinglooper.loopID
        trier.attempt({
            until: () ->
                return ! (myID==thumbloader.loadinglooper.loopID and thumbloader.alive())
            ,
            action: () ->
                if (myID==thumbloader.loadinglooper.loopID and thumbloader.alive())
                    thumbloader.comparifier()
            ,
            interval: -1000,
            limit: -1
        });



handleViewedItem= (data) ->
    thumbloader.finishComparifying $.parseJSON(data)

GetViewedItem= (foo) ->
    $.ajax foo,
        success: (data) ->
            handleViewedItem data





class window.thumbloader
    datalist: []
    constructor: (contentkind) ->
        @contentkind = contentkind
    
    loadinglooper: new loadinglooper

    remove: (pk) ->
       for i in [0...@.datalist.length]
           if "#{this.datalist[i][0]}" == "#{pk}"
               this.datalist.splice(i, 1)
    alive: () ->
        if this.datalist.length==0
            return false
        else
            return true

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        this.loadinglooper.loopID++
        this.loadinglooper.goloopy()

    comparifier: () ->
       request = ""
       for i in [0...@.datalist.length]
           request+="#{@.datalist[i][0]},"
     #### This line is where you will add support for different content types
       GetViewedItem("/ajax/#{this.contentkind}/#{request}")
       return null

    finishComparifying: (updata) ->
       for i in [0...updata.length]
           if updata[i].html
               replacelet= document.getElementsByClassName("pk=#{updata[i].pk}")
             ##  Make this a for loop or a way to do all of the array items!
               replacelet[0].innerHTML=updata[i].html
               this.remove(updata[i].pk)
           else
               console.log "i have no image........"

