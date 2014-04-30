

class loadinglooper
    alive: false
    reserect: false
    beginify: () ->
        if ! this.alive
            this.alive=true
            this.goloopy()
        else
            this.alive=false
            this.reserect=true
    dying: () ->
       if this.reserect
          this.reserect = false
          this.alive = true
          this.goloopy()
        
    goloopy: () ->
        trier.attempt({
            until: () ->
                return ! thumbloader.loadinglooper.alive
            ,
            action: () ->
                console.log "The Action is done!!! "
                thumbloader.comparifier()
            ,
            pass: () ->
                thumbloader.loadinglooper.dying()
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



console.log "I like tea!"


class window.thumbloader
    datalist: []
    loadinglooper: new loadinglooper

    alive: () ->
        if this.datalist.length<0
            return false
        else
            return true

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        this.loadinglooper.beginify()
        console.log this.datalist

    comparifier: () ->
       request = ""
       for i in [0...@.datalist.length]
           request+="#{@.datalist[i][0]},"
       console.log(request)
     #### This line is where you will add support for different content types
       GetViewedItem("/ajax/thumblist/#{request}")
       return null

    finishComparifying: (updata) ->
       for i in [0...updata.length]
           if updata[i].html
               console.log "I HAVE AN IMAGE!!!"
               console.log updata[i].pk
               console.log updata[i].html
           else
               console.log "i have no image........"
               console.log updata[i].pk

