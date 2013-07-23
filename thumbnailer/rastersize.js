var page = require('webpage').create(),
    system = require('system'),
    address, output, size;


    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: system.args[3], height: system.args[4] };

    page.open(address, function (status) {
        window.setTimeout(function () {
            page.render(output);
            phantom.exit();
        }, 200);
    });

