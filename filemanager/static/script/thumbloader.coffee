

handleViewedItem= (data) ->
    console.log $.parseJSON(data)[0].pk
    console.log $.parseJSON(data)[0].loading
    console.log $.parseJSON(data)[0].size[0]
    console.log $.parseJSON(data)[0].size[1]

GetViewedItem= (foo) ->
    $.ajax foo,
        success: (data) ->
            handleViewedItem data


$(document).ready(GetViewedItem("ajax/thumblist/1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10"))

console.log "I like tea!"

