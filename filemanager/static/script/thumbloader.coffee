

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

console.log "I like tea!"



class window.thumbloader
    datalist: []

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        console.log this.datalist
