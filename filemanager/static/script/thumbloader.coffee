

handleViewedItem= (data) ->
    console.log $.parseJSON(data)[0]

GetViewedItem= (foo) ->
    $.ajax  "ajax/thumblist/1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10",
        success: (data) ->
            handleViewedItem data

$(document).ready(GetViewedItem())

console.log "I like cake!"

