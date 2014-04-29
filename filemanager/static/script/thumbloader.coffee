

handleViewedItem= (data) ->
    console.log $.parseJSON(data)
    console.log $.parseJSON(data)[0].loading
    console.log $.parseJSON(data)[0].size[0]
    console.log $.parseJSON(data)[0].size[1]

GetViewedItem= (foo) ->
    $.ajax foo,
        success: (data) ->
            handleViewedItem data


$(document).ready(GetViewedItem("/ajax/thumblist/1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10"))

console.log "I like tea!"



class window.thumbloader
    datalist: []

    register: (pk, gallery) ->
        this.datalist.push([pk,gallery])
        console.log this.datalist
