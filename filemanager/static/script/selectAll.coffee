

# lets do this! Coffee script style!

# (by this, I mean the writing of a script for pretty selection)

        
class window.selectAllTool

    oldbox: null
    selected: null
    targetboxes: []
    newbox: null

    selectBoxes: () ->
        console.log("hi")
        console.log(this.targetboxes)
        console.log("hi")
        if this.selected
            console.log("hi")
            this.selected=false
            for element in this.targetboxes
                element.checked=true
        else
            this.selected=true
            for element in this.targetboxes
                element.checked=false

    startup: (allbox, targetboxes) ->
        this.selected=true
        this.targetboxes = document.getElementsByClassName(targetboxes)
        console.log(this.targetboxes)
        div = $ "<div>BleeBloo</div>"
        div.addClass "coffee-selectAllBox"
        this.oldbox = $(allbox)
        console.log(this.oldbox)
        this.oldbox.hide()
        div.click ->
          console.log("MURB")
          allBox.selectBoxes()
          this.selectBoxes()
        this.newbox = div
        this.oldbox.after(this.newbox)

