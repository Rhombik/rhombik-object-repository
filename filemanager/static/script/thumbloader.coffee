

startAttemptLoop = () ->
    i = 3
    console.log i
    trier.attempt({
        until: () ->
            if i < 0
                return true
            else
                return false
        ,
        action: () ->
            console.log "The Action is done!!! "+i+"th time"
            i=i-1
        ,
        interval: -1000,
        limit: -1
    });


handleViewedItem= (data) ->
    console.log $.parseJSON(data)
    console.log $.parseJSON(data)[0].loading
    console.log $.parseJSON(data)[0].size[0]
    console.log $.parseJSON(data)[0].size[1]

GetViewedItem= (foo) ->
    $.ajax foo,
        success: (data) ->
            handleViewedItem data


$(document).ready(GetViewedItem("/ajax/thumblist/1,2,3,4,5,6,7,8,9,10"))


$(document).ready(startAttemptLoop)

console.log "I like tea!"



class window.thumbloader
    datalist: []

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        console.log this.datalist
