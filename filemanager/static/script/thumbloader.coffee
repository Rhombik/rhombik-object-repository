

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
    awake: false
    datalist: []
    constructor: (contentkind) ->
        @contentkind = contentkind
    
    loadinglooper: new loadinglooper

    wakeUp: () ->
        this.awake = true
        this.loadinglooper.goloopy()

    remove: (pk) ->
       # console.log "I'm trying to kill pic with pk #{pk}"
       listlength=this.datalist.length
       i=0
       killed=false
       while i < listlength
           if "#{this.datalist[i][0]}" == "#{pk}"
               # console.log "I killed #{this.datalist[i][0]}"
               this.datalist.splice(i, 1)
               killed=true
               break
           i++
       if ! killed
           console.log "Thumbloader failed to delete pic with pk #{pk}. This should not have happened."

    alive: () ->
        if this.datalist.length==0
            return false
        else
            return true

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        if this.awake
          this.loadinglooper.loopID++
          this.loadinglooper.goloopy()

    comparifier: () ->
       request = ""
       for i in [0...this.datalist.length]
           request+="#{this.datalist[i][0]},"
       GetViewedItem("/ajax/#{this.contentkind}/#{request}")

    finishComparifying: (updata) ->
       killem=[]
       for i in [0...updata.length]
           if updata[i].html
               replacelet= document.getElementsByClassName("pk=#{updata[i].pk}")
             ##  Make this a for loop or a way to do all of the array items!
               replacelet[0].innerHTML=updata[i].html
               killem.push(updata[i].pk)
       for i in [0...killem.length]
           this.remove(killem[i])

