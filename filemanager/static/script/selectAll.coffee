

# lets do this! Coffee script style!

# (by this, I mean the writing of a script for pretty selection)

setElementsSelected = (array,select) ->
    console.log("hi")
    console.log(array)
    if select
        for element in array
            element.checked=true
    else
        for element in array
            element.checked=false
        
toggleGlobalSelect: (array,targetboxes, value) ->
        console.log("got here")
        if selected
            @selected=false
            setElementsSelected(array,targetboxes, true)
        else
            @selected=true
            setElementsSelected(array,targetboxes, false)

class window.selectAllTool
    oldbox=null
    selected=null
    targetboxes=null
    newbox=null

    constructor: () ->

    startup: (allbox, targetboxes) ->
        @selected=false
        @targetboxes = document.getElementsByClassName(targetboxes)
        console.log(@targetboxes)
        div = $ "<div>BleeBloo</div>"
        div.addClass "coffee-selectAllBox"
        @oldbox = $(allbox)
        console.log(@oldbox)
        @oldbox.hide()
        div.click ->
          console.log("MURB")
          setElementsSelected(@targetboxes,@selected)
          @selected.toggle
        @newbox = div
        @oldbox.after(@newbox)

